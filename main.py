import urllib.request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from supabase import create_client, Client

# IMPORT ARSITEKTUR FOLDER 'src/'
from src.models.instrumen import TeleskopOptik, TeleskopRadio
from src.core.exceptions import CuacaTidakLayakError, JadwalInstrumenBentrokError

# ==========================================
# KONFIGURASI SUPABASE (JALAN NINJA)
# ==========================================
# TEMPELKAN URL DAN KEY SUPABASE-MU DI SINI (Pastikan pakai tanda kutip " ")
SUPABASE_URL = "https://hpkwmngrrygyslhjfjpq.supabase.co" 
SUPABASE_KEY = "sb_publishable_MrBy-lzZPMRHO3q3JDFeyg_fhTNxOko" 

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ... (lanjutkan dengan sisa kodemu yang ada di bawahnya, seperti fungsi cuaca dll) ...

# Inisialisasi klien Supabase (Akan gagal jika key belum diisi di Vercel)
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("Peringatan: Kunci Supabase belum dikonfigurasi!")

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
    return {"status": "Peladen Backend terhubung ke Supabase dengan aman!"}

# ==========================================
# MEMBACA KATALOG INSTRUMEN (Tetap Statis)
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

# ==========================================
# ENDPOINT API (SUPABASE INTEGRATION)
# ==========================================
@app.get("/api/jadwal")
def get_semua_jadwal():
    try:
        # Mengambil seluruh data dari Supabase
        response = supabase.table("jadwal_observasi").select("*").execute()
        return response.data
    except Exception as e:
        return []

@app.post("/api/jadwal")
def ajukan_proposal(proposal: Proposal):
    id_inst_backend = "OPT01" if proposal.instrumen == "Teleskop Optik" else "RAD01"
    
    if id_inst_backend not in katalog_instrumen:
        raise HTTPException(status_code=404, detail="Instrumen tidak ditemukan.")
        
    instrumen = katalog_instrumen[id_inst_backend]
    
    # 1. Validasi Cuaca & Alat (Logika PBO)
    try:
        if id_inst_backend == "RAD01":
            if hasattr(instrumen, "set_status_instrumen"):
                instrumen.set_status_instrumen("Dalam Perbaikan (Maintenance)")
            raise CuacaTidakLayakError("Instrumen Teleskop Radio sedang dalam pemeliharaan.")
            
        instrumen.hitung_kelayakan_pengamatan(proposal.cuaca, 45.0, "Cembung")
    except CuacaTidakLayakError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    # 2. Validasi Bentrok dari Supabase
    try:
        jadwal_lama = supabase.table("jadwal_observasi").select("*").execute().data
        
        for j in jadwal_lama:
            if j.get("instrumen") == proposal.instrumen:
                if not (proposal.jam_selesai <= int(j["jam_mulai"]) or proposal.jam_mulai >= int(j["jam_selesai"])):
                    raise JadwalInstrumenBentrokError(
                        f"Bentrok! {proposal.instrumen} dipakai pada jam {j['jam_mulai']}:00 - {j['jam_selesai']}:00."
                    )
        
        # 3. Simpan ke Supabase jika lolos semua ujian
        data_baru = proposal.dict()
        supabase.table("jadwal_observasi").insert(data_baru).execute()
            
        return {"pesan": f"Proposal {proposal.id_proposal} berhasil diamankan di Cloud!"}
    
    except JadwalInstrumenBentrokError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Supabase: {str(e)}")

@app.delete("/api/jadwal/{id_proposal}")
def hapus_proposal(id_proposal: str):
    try:
        # Hapus berdasarkan ID
        response = supabase.table("jadwal_observasi").delete().eq("id_proposal", id_proposal).execute()
        if not response.data:
             raise HTTPException(status_code=404, detail="Data tidak ditemukan.")
        return {"pesan": f"Proposal {id_proposal} berhasil dibatalkan."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")