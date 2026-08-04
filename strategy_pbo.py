import csv
from abc import ABC, abstractmethod
from typing import List, Dict

# 1. Strategy Interface
class StrategiEkspor(ABC):
    @abstractmethod
    def ekspor(self, data: List[Dict], filepath: str):
        pass

# 2. Concrete Strategy A: Ekspor ke CSV
class EksporCSV(StrategiEkspor):
    def ekspor(self, data: List[Dict], filepath: str):
        if not data:
            return
        # Mengambil header dari keys dictionary
        keys = data[0].keys()
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

# 3. Concrete Strategy B: Ekspor ke TXT (Sebagai bukti fleksibilitas)
class EksporTXT(StrategiEkspor):
    def ekspor(self, data: List[Dict], filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(f"ID: {item.get('id_proposal')} | Objek: {item.get('target_objek')} | Jam: {item.get('waktu_mulai')}-{item.get('waktu_selesai')}\n")

# 4. Context Class
class LaporanPengamatan:
    def __init__(self, strategi: StrategiEkspor):
        self._strategi = strategi  # Injeksi dependensi strategi

    def set_strategi(self, strategi: StrategiEkspor):
        self._strategi = strategi

    def buat_laporan(self, data: List[Dict], filepath: str):
        self._strategi.ekspor(data, filepath)