# File: main_api.py
import urllib.request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import datetime

# 1. IMPORT ARSITEKTUR FOLDER 'src/' (TeleskopRadio asli diimpor dari sini)
from src.models.instrumen import TeleskopOptik, TeleskopRadio, KameraLangit
from src.core.exceptions import CuacaTidakLayakError, JadwalInstrumenBentrokError
from src.utils.file_handler import LaporanPengamatan, EksporCSV

def dapatkan_cuaca_lhokseumawe() -> str:
    """Mengambil data cuaca real-time di langit Lhokseumawe menggunakan Open-Meteo API."""
    # Koordinat Lhokseumawe: Latitude 5.1801, Longitude 97.1507
    url = "https://api.open-meteo.com/v1/forecast?latitude=5.1801&longitude=97.1507&current_weather=true"
    
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            kode_cuaca = data['current_weather']['weathercode']
            
            # Menerjemahkan kode WMO ke format sistem kita
            if kode_cuaca == 0: 
                return "Cerah"
            elif 1 <= kode_cuaca <= 3: 
                return "Berawan"
            elif 51 <= kode_cuaca <= 67 or 80 <= kode_cuaca <= 82: 
                return "Hujan"
            elif kode_cuaca >= 95: 
                return "Badai Petir"
            else: 
                return "Cerah" # Default aman
    except Exception as e:
        print(f"Gagal mengambil cuaca live: {e}")
        return "Cerah" # Fallback jika tidak ada internet

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# FILE HANDLING: Membaca instrumen.json
# ==========================================
katalog_instrumen = {}
os.makedirs("data", exist_ok=True)

try:
    with open("data/instrumen.json", "r") as f:
        data_inst = json.load(f)
        for item in data_inst:
            if item["tipe"] == "Optik":
                katalog_instrumen[item["id_instrumen"]] = TeleskopOptik(item["id_instrumen"], item["nama"], item["batas_mag"])
            elif item["tipe"] == "Radio":
                katalog_instrumen[item["id_instrumen"]] = TeleskopRadio(item["id_instrumen"], item["nama"], item["batas_mag"])
except FileNotFoundError:
    print("File instrumen.json tidak ditemukan, menggunakan data default.")
    katalog_instrumen["OPT01"] = TeleskopOptik("OPT01", "Teleskop Optik Utama", 22.5)
    katalog_instrumen["RAD01"] = TeleskopRadio("RAD01", "Teleskop Radio Utama", 30.0)

# ==========================================
# SKEMA DATA (Pydantic BaseModel)
# ==========================================
class Proposal(BaseModel):
    id_proposal: str
    id_instrumen: str
    waktu_mulai: int
    waktu_selesai: int
    target_objek: str
    cuaca: str
    
    # Entitas Skenario dengan nilai default
    nama_operator: str = "Muhammad Luthfi Fadil"
    id_kubah: str = "KUB-01"

@app.get("/api/cuaca-live")
def get_cuaca_live():
    cuaca_sekarang = dapatkan_cuaca_lhokseumawe()
    return {"lokasi": "Lhokseumawe, Aceh", "cuaca": cuaca_sekarang}

# ==========================================
# ENDPOINT API
# ==========================================
@app.get("/api/jadwal")
def get_semua_jadwal():
    try:
        with open("data/jadwal_observasi.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def catat_kegagalan(proposal_dict: dict, alasan_gagal: str):
    """Mencatat setiap proposal yang ditolak ke dalam JSON."""
    if not os.path.exists("data"):
        os.makedirs("data")
        
    file_log = "data/observasi_gagal.json"
    data_gagal = []
    
    if os.path.exists(file_log):
        try:
            with open(file_log, "r") as f:
                data_gagal = json.load(f)
        except json.JSONDecodeError:
            data_gagal = []
            
    proposal_dict["alasan_penolakan"] = alasan_gagal
    proposal_dict["waktu_tercatat"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data_gagal.append(proposal_dict)
    
    with open(file_log, "w") as f:
        json.dump(data_gagal, f, indent=4)

@app.post("/api/proposal")
def ajukan_proposal(proposal: Proposal):
    if proposal.id_instrumen not in katalog_instrumen:
        raise HTTPException(status_code=404, detail=f"Instrumen {proposal.id_instrumen} tidak dikenali.")
        
    instrumen = katalog_instrumen[proposal.id_instrumen]
    
    # Validasi Polimorfisme, Cuaca, & Kondisi Alat (Digabung secara bersih)
    try:
        # Simulasi pengujian: Jika instrumen RAD01 dipilih, uji penolakan status
        if proposal.id_instrumen == "RAD01":
            # Memeriksa apakah method set_status_instrumen tersedia di objek instrumen
            if hasattr(instrumen, "set_status_instrumen"):
                instrumen.set_status_instrumen("Dalam Perbaikan (Maintenance)")
            raise CuacaTidakLayakError("Instrumen RAD01 sedang dalam pemeliharaan (Maintenance).")
            
        instrumen.hitung_kelayakan_pengamatan(proposal.cuaca, 45.0, "Cembung")
        
    except CuacaTidakLayakError as e:
        # PENCATATAN KEGAGALAN OTOMATIS
        catat_kegagalan(proposal.dict(), str(e))
        raise HTTPException(status_code=400, detail=str(e))
        
    # Validasi Bentrok Waktu & Penyimpanan Alur Normal
    try:
        jadwal_lama = []
        if os.path.exists("data/jadwal_observasi.json"):
            with open("data/jadwal_observasi.json", "r") as f:
                jadwal_lama = json.load(f)
        
        for j in jadwal_lama:
            if j["id_instrumen"] == proposal.id_instrumen:
                if not (proposal.waktu_selesai <= j["waktu_mulai"] or proposal.waktu_mulai >= j["waktu_selesai"]):
                    raise JadwalInstrumenBentrokError(
                        f"Bentrok! {proposal.id_instrumen} dipakai pada jam {j['waktu_mulai']}:00-{j['waktu_selesai']}:00."
                    )
        
        # Simpan ke JSON
        data_baru = proposal.dict()
        jadwal_lama.append(data_baru)
        with open("data/jadwal_observasi.json", "w") as f:
            json.dump(jadwal_lama, f, indent=4)
            
        laporan = LaporanPengamatan(EksporCSV())
        laporan.buat_laporan(jadwal_lama, "data/hasil_pengamatan.csv")
            
        return {"pesan": f"Proposal {proposal.id_proposal} disetujui. Laporan CSV diekspor!"}
    
    except JadwalInstrumenBentrokError as e:
        catat_kegagalan(proposal.dict(), str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error File Handling: {str(e)}")
    
@app.delete("/api/proposal/{id_proposal}")
def hapus_proposal(id_proposal: str):
    try:
        if os.path.exists("data/jadwal_observasi.json"):
            with open("data/jadwal_observasi.json", "r") as f:
                jadwal_lama = json.load(f)
            
            jadwal_baru = [j for j in jadwal_lama if j["id_proposal"] != id_proposal]
            
            with open("data/jadwal_observasi.json", "w") as f:
                json.dump(jadwal_baru, f, indent=4)
            
            laporan = LaporanPengamatan(EksporCSV())
            laporan.buat_laporan(jadwal_baru, "data/hasil_pengamatan.csv")
            
            return {"pesan": f"Proposal {id_proposal} berhasil dibatalkan."}
        
        raise HTTPException(status_code=404, detail="Data tidak ditemukan.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")