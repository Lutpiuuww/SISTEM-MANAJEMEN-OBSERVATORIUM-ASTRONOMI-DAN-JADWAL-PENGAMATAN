from abc import ABC, abstractmethod

# ==========================================
# 1. CUSTOM EXCEPTIONS (Wajib dari dosen)
# ==========================================
class CuacaTidakLayakError(Exception):
    """Dilemparkan ketika cuaca tidak mendukung untuk observasi."""
    pass

class JadwalInstrumenBentrokError(Exception):
    """Dilemparkan ketika proposal menabrak jadwal yang sudah ada."""
    pass

# ==========================================
# 2. ENKAPSULASI & SUPERCLASS (Wajib)
# ==========================================
class InstrumenAstronomi(ABC):
    def __init__(self, id_instrumen: str, nama: str, status: str, batas_mag: float):
        self.id_instrumen = id_instrumen
        self.nama = nama
        
        # Atribut Private (Enkapsulasi - Wajib sesuai rubrik)
        self.__status_instrumen = status
        self.__batas_magnitudo = batas_mag

    # Getter & Setter menggunakan property
    @property
    def status_instrumen(self):
        return self.__status_instrumen
    
    @status_instrumen.setter
    def status_instrumen(self, nilai: str):
        if nilai not in ["Aktif", "Perawatan", "Rusak"]:
            raise ValueError("Status tidak valid!")
        self.__status_instrumen = nilai

    @property
    def batas_magnitudo(self):
        return self.__batas_magnitudo

    # Method Abstract untuk Polimorfisme
    # Di dalam class InstrumenAstronomi(ABC):
    @abstractmethod
    def hitung_kelayakan_pengamatan(self, cuaca: str, elevasi: float, fase_bulan: str) -> bool:
        pass

# ==========================================
# 3. INHERITANCE & POLIMORFISME (Wajib)
# ==========================================
class TeleskopOptik(InstrumenAstronomi):
    def hitung_kelayakan_pengamatan(self, cuaca: str, elevasi: float, fase_bulan: str) -> bool:
        if self.status_instrumen != "Aktif":
            return False
        # Validasi Polimorfisme spesifik Optik
        if cuaca.lower() != "cerah":
            raise CuacaTidakLayakError(f"Teleskop Optik butuh cuaca cerah. Saat ini: {cuaca}")
        if fase_bulan.lower() == "purnama" and elevasi < 30:
            raise CuacaTidakLayakError("Cahaya purnama terlalu terang untuk elevasi rendah.")
        return True

class TeleskopRadio(InstrumenAstronomi):
    def hitung_kelayakan_pengamatan(self, cuaca: str, elevasi: float, fase_bulan: str) -> bool:
        if self.status_instrumen != "Aktif":
            return False
        # Radio kebal fase bulan, tapi benci badai petir
        if cuaca.lower() == "badai petir":
            raise CuacaTidakLayakError("Teleskop Radio tidak bisa beroperasi saat badai petir.")
        if elevasi < 15:
            raise CuacaTidakLayakError("Elevasi terlalu rendah, terhalang bukit observatorium.")
        return True

class KameraLangit(InstrumenAstronomi):
    def hitung_kelayakan_pengamatan(self, cuaca: str, elevasi: float, fase_bulan: str) -> bool:
        if self.status_instrumen != "Aktif":
            return False
        if cuaca.lower() in ["hujan", "badai petir", "berawan"]:
            raise CuacaTidakLayakError(f"Kamera Langit terhalang awan/hujan.")
        return True