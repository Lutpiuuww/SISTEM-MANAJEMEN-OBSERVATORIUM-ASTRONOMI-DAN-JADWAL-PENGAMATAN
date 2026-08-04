# src/models/pengamatan.py

from core.exceptions import JadwalInstrumenBentrokError

class ProposalPengamatan:
    """Representasi pengajuan jadwal dari astronom."""
    def __init__(self, id_proposal: str, id_instrumen: str, waktu_mulai: int, waktu_selesai: int, target_objek: str):
        self.id_proposal = id_proposal
        self.id_instrumen = id_instrumen
        self.waktu_mulai = waktu_mulai     # Format jam sederhana (0-23) untuk CLI
        self.waktu_selesai = waktu_selesai # Format jam sederhana (0-23) untuk CLI
        self.target_objek = target_objek
        self.status = "Menunggu Validasi"

    def to_dict(self):
        """Konversi ke dictionary untuk disimpan ke JSON."""
        return {
            "id_proposal": self.id_proposal,
            "id_instrumen": self.id_instrumen,
            "waktu_mulai": self.waktu_mulai,
            "waktu_selesai": self.waktu_selesai,
            "target_objek": self.target_objek,
            "status": self.status
        }


class ManajerJadwal:
    """Mengelola logika penjadwalan dan mencegah bentrokan."""
    def __init__(self, db_handler):
        self.db = db_handler # Injeksi dependensi FileHandler
        self.file_jadwal = "jadwal_observasi.json"

    def validasi_bentrok(self, proposal_baru: ProposalPengamatan):
        """Mengecek apakah jadwal baru bentrok dengan jadwal yang sudah disetujui."""
        jadwal_aktif = self.db.baca_json(self.file_jadwal)
        
        for jadwal in jadwal_aktif:
            # Hanya cek instrumen yang sama dan sudah disetujui
            if jadwal['id_instrumen'] == proposal_baru.id_instrumen and jadwal['status'] == "Disetujui":
                # Logika bentrokan waktu (overlap)
                if max(proposal_baru.waktu_mulai, jadwal['waktu_mulai']) < min(proposal_baru.waktu_selesai, jadwal['waktu_selesai']):
                    raise JadwalInstrumenBentrokError(
                        f"Gagal! Instrumen {proposal_baru.id_instrumen} sudah dibooking pada jam "
                        f"{jadwal['waktu_mulai']}-{jadwal['waktu_selesai']} (Proposal: {jadwal['id_proposal']})."
                    )

    def ajukan_proposal(self, proposal: ProposalPengamatan):
        """Memvalidasi dan menyimpan proposal jika tidak bentrok."""
        try:
            self.validasi_bentrok(proposal)
            proposal.status = "Disetujui"
            
            # Simpan jadwal baru
            semua_jadwal = self.db.baca_json(self.file_jadwal)
            semua_jadwal.append(proposal.to_dict())
            self.db.simpan_json(self.file_jadwal, semua_jadwal)
            
            print(f"Sukses: Proposal {proposal.id_proposal} disetujui dan dijadwalkan.")
            return True
            
        except JadwalInstrumenBentrokError as e:
             proposal.status = "Ditolak (Bentrok)"
             print(e)
             return False