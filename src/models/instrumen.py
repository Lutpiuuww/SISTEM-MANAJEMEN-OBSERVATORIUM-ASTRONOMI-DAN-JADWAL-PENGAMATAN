# File: src/models/instrumen.py

from abc import ABC, abstractmethod
from src.core.exceptions import CuacaTidakLayakError

class InstrumenAstronomi(ABC):
    """
    Superclass abstrak untuk semua instrumen di observatorium.
    Menerapkan encapsulation untuk status dan batas magnitudo.
    """
    def __init__(self, id_instrumen: str, nama_instrumen: str, batas_magnitudo: float):
        self.id_instrumen = id_instrumen
        self.nama_instrumen = nama_instrumen
        
        # --- ENCAPSULATION WAJIB ---
        # Atribut dilindungi dengan prefix dunder (double underscore) '__'
        self.__status_instrumen = "Tersedia" 
        self.__batas_magnitudo = batas_magnitudo

    # --- GETTER & SETTER untuk __status_instrumen ---
    @property
    def status_instrumen(self) -> str:
        return self.__status_instrumen

    @status_instrumen.setter
    def status_instrumen(self, status_baru: str):
        status_valid = ["Tersedia", "Digunakan", "Pemeliharaan"]
        if status_baru in status_valid:
            self.__status_instrumen = status_baru
        else:
            raise ValueError(f"Status tidak valid. Harap pilih dari: {status_valid}")

    # --- GETTER & SETTER untuk __batas_magnitudo ---
    @property
    def batas_magnitudo(self) -> float:
        return self.__batas_magnitudo

    @batas_magnitudo.setter
    def batas_magnitudo(self, nilai_baru: float):
        if nilai_baru > 0:
            self.__batas_magnitudo = nilai_baru
        else:
            raise ValueError("Batas magnitudo harus berupa angka positif.")

    # --- POLYMORPHISM WAJIB ---
    # Method abstrak ini wajib di-override oleh semua subclass
    @abstractmethod
    def hitung_kelayakan_pengamatan(self, cuaca: str, elevasi: float, fase_bulan: str) -> bool:
        """
        Menghitung apakah instrumen bisa digunakan berdasarkan 4 syarat wajib:
        cuaca simulasi, elevasi objek, fase bulan, dan kondisi alat.
        """
        pass
        
    def __str__(self):
        return f"[{self.id_instrumen}] {self.nama_instrumen} - Status: {self.__status_instrumen}"


# =====================================================================
# SUBCLASS IMPLEMENTASI POLIMORFISME
# =====================================================================

class TeleskopOptik(InstrumenAstronomi):
    def __init__(self, id_instrumen: str, nama_instrumen: str, batas_magnitudo: float, panjang_fokus: float = 1000):
        super().__init__(id_instrumen, nama_instrumen, batas_magnitudo)
        self.panjang_fokus = panjang_fokus

    # --- POLYMORPHISM: Implementasi khusus untuk TeleskopOptik ---
    def hitung_kelayakan_pengamatan(self, cuaca: str, elevasi: float, fase_bulan: str) -> bool:
        # Syarat 1: Kondisi Alat
        if self.status_instrumen != "Tersedia":
            return False
            
        # Syarat 2: Cuaca
        if cuaca.lower() != "cerah":
            raise CuacaTidakLayakError(f"Teleskop Optik butuh cuaca cerah. Saat ini: {cuaca}")
            
        # Syarat 3 & 4: Fase Bulan dan Elevasi
        if fase_bulan.lower() == "purnama" and elevasi < 30:
            raise CuacaTidakLayakError("Cahaya purnama terlalu terang untuk objek berelevasi rendah (Teleskop Optik).")
            
        return True


class TeleskopRadio(InstrumenAstronomi):
    def __init__(self, id_instrumen: str, nama_instrumen: str, batas_magnitudo: float, rentang_frekuensi: str = "1-10 GHz"):
        super().__init__(id_instrumen, nama_instrumen, batas_magnitudo)
        self.rentang_frekuensi = rentang_frekuensi

    # --- POLYMORPHISM: Implementasi khusus untuk TeleskopRadio ---
    def hitung_kelayakan_pengamatan(self, cuaca: str, elevasi: float, fase_bulan: str) -> bool:
        if self.status_instrumen != "Tersedia":
            return False
            
        if cuaca.lower() == "badai petir":
            raise CuacaTidakLayakError("Teleskop Radio tidak bisa beroperasi saat badai petir (bahaya statis dan distorsi frekuensi).")
            
        if elevasi < 15:
            raise CuacaTidakLayakError("Elevasi terlalu rendah, sinyal terhalang oleh kontur daratan/bukit sekitar.")
            
        return True


class KameraLangit(InstrumenAstronomi):
    """
    Kamera All-Sky (biasanya untuk memantau meteor atau cuaca lokal).
    """
    def __init__(self, id_instrumen: str, nama_instrumen: str, batas_magnitudo: float, field_of_view: float = 180):
         super().__init__(id_instrumen, nama_instrumen, batas_magnitudo)
         self.field_of_view = field_of_view 

    # --- POLYMORPHISM: Implementasi khusus untuk KameraLangit ---
    def hitung_kelayakan_pengamatan(self, cuaca: str, elevasi: float, fase_bulan: str) -> bool:
        if self.status_instrumen != "Tersedia":
            return False
            
        if cuaca.lower() in ["hujan", "badai petir", "berawan"]:
             raise CuacaTidakLayakError("Lensa Kamera Langit terhalang oleh awan atau hujan.")
             
        return True