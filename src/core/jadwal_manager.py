# src/core/jadwal_manager.py
from src.exceptions import JadwalBentrokError

class JadwalManager:
    def __init__(self):
        self.__daftar_jadwal = []
    
    def get_semua_jadwal(self):
        return self.__daftar_jadwal

    def tambah_jadwal(self, jadwal_baru: dict):
        for jadwal in self.__daftar_jadwal:
            if jadwal['jam_mulai'] == jadwal_baru['jam_mulai']:
                raise JadwalBentrokError(jadwal_baru['jam_mulai'])
        
        self.__daftar_jadwal.append(jadwal_baru)