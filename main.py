# File: main.py
import urllib.request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import datetime

# IMPORT ARSITEKTUR FOLDER 'src/'
from src.models.instrumen import TeleskopOptik, TeleskopRadio, KameraLangit
from src.core.exceptions import CuacaTidakLayakError, JadwalInstrumenBentrokError
from src.utils.file_handler import LaporanPengamatan, EksporCSV

# ==========================================
# KONFIGURASI VERCEL (WRITABLE DIRECTORY)
# Vercel hanya mengizinkan penulisan di folder /tmp/
# ==========================================
WRITABLE_DIR = "/tmp"
FILE_JADWAL = f"{WRITABLE_DIR}/jadwal_observasi.json"
FILE_GAGAL = f"{WRITABLE_DIR}/observasi_gagal.json"
FILE_CSV = f"{WRITABLE_DIR}/hasil_pengamatan.csv"

def dapatkan_cuaca_lhokseumawe() -> str:
    url = "https://api.open-meteo.com/v1/forecast?latitude=5.1801&longitude=97.1507&current_weather=true"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            kode_cuaca = data['current_weather']['weathercode']
            
            if kode_cuaca == 0: return "Cerah"
            elif 1 <= kode_cuaca <= 3: return "Berawan"
            elif 51 <= kode_cuaca <= 67 or 80 <= kode_cuaca <= 82: return "Hujan"
            elif kode_cuaca >= 95: return "Badai Petir"
            else: return "Cerah"
    except Exception as e:
        print(f"Gagal mengambil cuaca: {e}")
        return "Cerah"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False, # <--- UBAH INI JADI False
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tambahkan rute ini di bawah middleware agar halaman depanmu terlihat keren
@app.get("/")
def halaman_depan():
    return {"status": "Peladen Backend Observatorium Berjalan Sempurna di Vercel!"}

# ==========================================
# MEMBACA INSTRUMEN (Tetap dari folder 'data/' karena file statis bawaan GitHub)
# ==========================================
katalog_instrumen = {}
try:
    with open("data/instrumen.json", "r") as f:
        data_inst = json.load(f)
        for item in data_inst:
            if item["tipe"] == "Optik":
                katalog_instrumen[item["id_instrumen"]] = TeleskopOptik(item["id_instrumen"], item["nama"], item["batas_mag"])
            elif item["tipe"] == "Radio":
                katalog_instrumen[item["id_instrumen"]] = TeleskopRadio(item["id_instrumen"], item["nama"], item["batas_mag"])
except FileNotFoundError:
    katalog_instrumen["OPT01"] = TeleskopOptik("OPT01", "Teleskop Optik Utama", 22.5)
    katalog_instrumen["RAD01"] = TeleskopRadio("RAD01", "Teleskop Radio Utama", 30.0)

# ==========================================
# SKEMA DATA
# ==========================================
class Proposal(BaseModel):
    id_proposal: str
    target_objek: str
    jam_mulai: int
    jam_selesai: int
    instrumen: str
    cuaca: str
    nama_operator: str = "Muhammad Luthfi Fadil"
    id_kubah: str = "KUB-01"

@app.get("/api/cuaca-live")
def get_cuaca_live():
    return {"lokasi": "Lhokseumawe, Aceh", "cuaca": dapatkan_cuaca_lhokseumawe()}

def catat_kegagalan(proposal_dict: dict, alasan_gagal: str):
    """Mencatat proposal gagal ke folder /tmp/ Vercel"""
    data_gagal = []
    if os.path.exists(FILE_GAGAL):
        try:
            with open(FILE_GAGAL, "r") as f:
                data_gagal = json.load(f)
        except: pass
            
    proposal_dict["alasan_penolakan"] = alasan_gagal
    proposal_dict["waktu_tercatat"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_gagal.append(proposal_dict)
    
    with open(FILE_GAGAL, "w") as f:
        json.dump(data_gagal, f, indent=4)

# ==========================================
# ENDPOINT API 
# ==========================================
@app.get("/api/jadwal")
def get_semua_jadwal():
    try:
        with open(FILE_JADWAL, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.post("/api/jadwal")
def ajukan_proposal(proposal: Proposal):
    id_inst_backend = "OPT01" if proposal.instrumen == "Teleskop Optik" else "RAD01"
    
    if id_inst_backend not in katalog_instrumen:
        raise HTTPException(status_code=404, detail=f"Instrumen tidak ditemukan.")
        
    instrumen = katalog_instrumen[id_inst_backend]
    
    try:
        if id_inst_backend == "RAD01":
            if hasattr(instrumen, "set_status_instrumen"):
                instrumen.set_status_instrumen("Dalam Perbaikan (Maintenance)")
            raise CuacaTidakLayakError("Instrumen Teleskop Radio sedang dalam pemeliharaan (Maintenance).")
            
        instrumen.hitung_kelayakan_pengamatan(proposal.cuaca, 45.0, "Cembung")
        
    except CuacaTidakLayakError as e:
        catat_kegagalan(proposal.dict(), str(e))
        raise HTTPException(status_code=400, detail=str(e))
        
    try:
        jadwal_lama = []
        if os.path.exists(FILE_JADWAL):
            with open(FILE_JADWAL, "r") as f:
                jadwal_lama = json.load(f)
        
        for j in jadwal_lama:
            if j.get("instrumen") == proposal.instrumen:
                if not (proposal.jam_selesai <= int(j["jam_mulai"]) or proposal.jam_mulai >= int(j["jam_selesai"])):
                    raise JadwalInstrumenBentrokError(
                        f"Bentrok! {proposal.instrumen} sudah dijadwalkan pada jam {j['jam_mulai']}:00 - {j['jam_selesai']}:00."
                    )
        
        data_baru = proposal.dict()
        jadwal_lama.append(data_baru)
        
        # Simpan ke folder /tmp/ Vercel
        with open(FILE_JADWAL, "w") as f:
            json.dump(jadwal_lama, f, indent=4)
            
        laporan = LaporanPengamatan(EksporCSV())
        laporan.buat_laporan(jadwal_lama, FILE_CSV)
            
        return {"pesan": f"Proposal {proposal.id_proposal} disetujui. Laporan CSV diekspor!"}
    
    except JadwalInstrumenBentrokError as e:
        catat_kegagalan(proposal.dict(), str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Sistem: {str(e)}")

@app.delete("/api/jadwal/{id_proposal}")
def hapus_proposal(id_proposal: str):
    try:
        if os.path.exists(FILE_JADWAL):
            with open(FILE_JADWAL, "r") as f:
                jadwal_lama = json.load(f)
            
            jadwal_baru = [j for j in jadwal_lama if j["id_proposal"] != id_proposal]
            
            with open(FILE_JADWAL, "w") as f:
                json.dump(jadwal_baru, f, indent=4)
            
            laporan = LaporanPengamatan(EksporCSV())
            laporan.buat_laporan(jadwal_baru, FILE_CSV)
            
            return {"pesan": f"Proposal {id_proposal} berhasil dibatalkan."}
        
        raise HTTPException(status_code=404, detail="Data tidak ditemukan.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")