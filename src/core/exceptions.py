# src/core/exceptions.py

class CuacaTidakLayakError(Exception):
    def __init__(self, pesan="Cuaca tidak memenuhi standar kelayakan untuk instrumen ini."):
        self.pesan = pesan
        super().__init__(self.pesan)


class JadwalInstrumenBentrokError(Exception):
    def __init__(self, pesan="Gagal menjadwalkan: Waktu observasi bentrok dengan jadwal yang sudah ada."):
        self.pesan = pesan
        super().__init__(self.pesan)