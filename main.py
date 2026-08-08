import urllib.request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import datetime

from src.models.instrumen import TeleskopOptik, TeleskopRadio, KameraLangit
from src.core.exceptions import CuacaTidakLayakError, JadwalInstrumenBentrokError
# LaporanPengamatan CSV sementara dinonaktifkan di memori agar Vercel tidak crash
from src.utils.file_handler import LaporanPengamatan, EksporCSV

# ==========================================
# DATABASE SEMENTARA (IN-MEMORY RAM)
# Trik darurat agar data bertahan di Vercel tanpa File JSON
# ==========================================
DATABASE_JADWAL = []
DATABASE_GAGAL = []

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
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def halaman_depan():
    return {"status": "Peladen Backend Observatorium Berjalan Sempurna di Vercel!"}

# ==========================================
# MEMBACA KATALOG INSTRUMEN 
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
    proposal_dict["alasan_penolakan"] = alasan_gagal
    proposal_dict["waktu_tercatat"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    DATABASE_GAGAL.append(proposal_dict)

# ==========================================
# ENDPOINT API (MENGGUNAKAN RAM / VARIABEL GLOBAL)
# ==========================================
@app.get("/api/jadwal")
def get_semua_jadwal():
    return DATABASE_JADWAL

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
        # Validasi Bentrok langsung dari array RAM
        for j in DATABASE_JADWAL:
            if j.get("instrumen") == proposal.instrumen:
                if not (proposal.jam_selesai <= int(j["jam_mulai"]) or proposal.jam_mulai >= int(j["jam_selesai"])):
                    raise JadwalInstrumenBentrokError(
                        f"Bentrok! {proposal.instrumen} sudah dijadwalkan pada jam {j['jam_mulai']}:00 - {j['jam_selesai']}:00."
                    )
        
        data_baru = proposal.dict()
        DATABASE_JADWAL.append(data_baru) # Simpan ke variabel global
            
        return {"pesan": f"Proposal {proposal.id_proposal} disetujui."}
    
    except JadwalInstrumenBentrokError as e:
        catat_kegagalan(proposal.dict(), str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Sistem: {str(e)}")

@app.delete("/api/jadwal/{id_proposal}")
def hapus_proposal(id_proposal: str):
    global DATABASE_JADWAL
    
    jadwal_baru = [j for j in DATABASE_JADWAL if j["id_proposal"] != id_proposal]
    
    if len(jadwal_baru) == len(DATABASE_JADWAL):
         raise HTTPException(status_code=404, detail="Data tidak ditemukan.")
            
    DATABASE_JADWAL = jadwal_baru
    return {"pesan": f"Proposal {id_proposal} berhasil dibatalkan."}