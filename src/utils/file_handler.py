# File: src/utils/file_handler.py

import json
import csv
import os
from abc import ABC, abstractmethod
from typing import List, Dict

# =====================================================================
# 1. FILE HANDLING MURNI (Single Responsibility Principle)
# =====================================================================
class DatabaseLokal:
    def __init__(self, folder_data="data"):
        self.folder_data = folder_data
        if not os.path.exists(self.folder_data):
            os.makedirs(self.folder_data)

    def _get_path(self, nama_file: str) -> str:
        return os.path.join(self.folder_data, nama_file)

    def simpan_json(self, nama_file: str, data: list):
        """Menyimpan list of dictionary ke file JSON."""
        try:
            with open(self._get_path(nama_file), 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
             raise IOError(f"Gagal menyimpan ke {nama_file}: {e}")

    def baca_json(self, nama_file: str) -> list:
        """Membaca list of dictionary dari file JSON."""
        path_file = self._get_path(nama_file)
        if not os.path.exists(path_file):
            return [] # Kembalikan list kosong jika file belum ada
            
        try:
            with open(path_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Format JSON rusak pada file {nama_file}.")
        except Exception as e:
            raise IOError(f"Gagal membaca dari {nama_file}: {e}")

# =====================================================================
# 2. POLA DESAIN STRATEGY (Syarat Wajib Rubrik PBO)
# Menerapkan Open/Closed Principle (OCP)
# =====================================================================

# Strategy Interface
class StrategiEkspor(ABC):
    @abstractmethod
    def ekspor(self, data: List[Dict], filepath: str):
        pass

# Concrete Strategy A: Ekspor ke CSV
class EksporCSV(StrategiEkspor):
    def ekspor(self, data: List[Dict], filepath: str):
        if not data:
            return
        
        try:
            with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                # Mengambil fieldnames dari data terbaru (data paling akhir)
                # extrasaction='ignore' mencegah error jika ada atribut yang tidak rata
                fieldnames = list(data[-1].keys())
                
                writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
             raise IOError(f"Gagal menulis ke laporan CSV: {e}")

# Concrete Strategy B: Ekspor ke TXT
class EksporTXT(StrategiEkspor):
    def ekspor(self, data: List[Dict], filepath: str):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=== LAPORAN HASIL PENGAMATAN OBSERVATORIUM ===\n\n")
                for item in data:
                    f.write(f"ID Proposal : {item.get('id_proposal')}\n")
                    # Tambahan entitas baru untuk memenuhi skenario
                    f.write(f"Operator    : {item.get('nama_operator', 'Tidak Diketahui')}\n")
                    f.write(f"Kubah       : {item.get('id_kubah', 'Tidak Diketahui')}\n")
                    
                    f.write(f"Instrumen   : {item.get('id_instrumen')}\n")
                    f.write(f"Target      : {item.get('target_objek')}\n")
                    f.write(f"Cuaca       : {item.get('cuaca', 'Tidak Tersedia')}\n")
                    f.write(f"Waktu       : Jam {item.get('waktu_mulai')}:00 - {item.get('waktu_selesai')}:00\n")
                    f.write("-" * 45 + "\n")
        except Exception as e:
             raise IOError(f"Gagal menulis ke laporan TXT: {e}")

# Context Class
class LaporanPengamatan:
    def __init__(self, strategi: StrategiEkspor):
        self._strategi = strategi
        
    def set_strategi(self, strategi: StrategiEkspor):
        self._strategi = strategi
        
    def buat_laporan(self, data: List[Dict], filepath: str):
        self._strategi.ekspor(data, filepath)