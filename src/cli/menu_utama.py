# File: src/cli/menu_utama.py

import sys
from src.utils.file_handler import DatabaseLokal, LaporanPengamatan, EksporTXT, EksporCSV
from src.models.instrumen import TeleskopOptik, TeleskopRadio, KameraLangit
from src.core.exceptions import CuacaTidakLayakError, JadwalInstrumenBentrokError

class MenuCLI:
    def __init__(self):
        self.db = DatabaseLokal()
        # Inisialisasi Pola Desain Strategy untuk 2 jenis laporan
        self.laporan_txt = LaporanPengamatan(EksporTXT())
        self.laporan_csv = LaporanPengamatan(EksporCSV())
        
        # --- DATA AWAL ---
        self.instrumen_tersedia = {
            "OPT01": TeleskopOptik("OPT01", "Teleskop Reflektor 2M", batas_magnitudo=22.5),
            "RAD01": TeleskopRadio("RAD01", "Piringan Radio 20M", batas_magnitudo=30.0),
            "KAM01": KameraLangit("KAM01", "Kamera All-Sky 180", batas_magnitudo=15.0)
        }

    def tampilkan_header(self):
        print("\n" + "="*65)
        print("SISTEM MANAJEMEN OBSERVATORIUM ASTRONOMI".center(65))
        print("MUHAMMAD LUTHFI FADIL | 250180089".center(65))
        print("="*65)

    def menu_utama(self):
        while True:
            self.tampilkan_header()
            print("1. Lihat Daftar Instrumen")
            print("2. Ajukan Proposal Pengamatan (Operator & Kubah)")
            print("3. Eksekusi Pengamatan (Simulasi Cuaca PBO)")
            print("4. Cetak Laporan JSON ke TXT/CSV (Strategy Pattern)")
            print("0. Keluar")
            
            pilihan = input("\nPilih menu (0-4): ")
            
            if pilihan == '1':
                self.lihat_instrumen()
            elif pilihan == '2':
                self.buat_proposal()
            elif pilihan == '3':
                self.eksekusi_pengamatan()
            elif pilihan == '4':
                self.cetak_laporan()
            elif pilihan == '0':
                print("Sistem ditutup. Terima kasih.")
                sys.exit()
            else:
                print("Pilihan tidak valid.")

    def lihat_instrumen(self):
        print("\n--- DAFTAR INSTRUMEN ---")
        for instr in self.instrumen_tersedia.values():
            print(instr) 
        input("\nTekan Enter untuk kembali...")

    def buat_proposal(self):
        print("\n--- PENGAJUAN JADWAL (SKENARIO NORMAL & BENTROK) ---")
        id_prop = input("ID Proposal (misal: PR01): ")
        
        # --- TAMBAHAN ENTITAS OPERATOR & KUBAH ---
        nama_op = input("Nama Operator: ")
        id_kubah = input("ID Kubah Observatorium (KUB-01/KUB-02): ")
        
        id_inst = input("ID Instrumen (OPT01/RAD01/KAM01): ").upper()
        
        if id_inst not in self.instrumen_tersedia:
            print("❌ Error: Instrumen tidak ditemukan.")
            return
            
        try:
            mulai = int(input("Jam Mulai (0-23): "))
            selesai = int(input("Jam Selesai (0-23): "))
            objek = input("Target Objek (misal: Mars): ")
            
            # 1. Baca data lama dari JSON
            jadwal_lama = self.db.baca_json("jadwal_observasi.json")
            
            # 2. Logika Pengecekan Bentrok (Memicu Exception)
            for jadwal in jadwal_lama:
                if jadwal["id_instrumen"] == id_inst:
                    # Jika waktu beririsan, lempar error
                    if not (selesai <= jadwal["waktu_mulai"] or mulai >= jadwal["waktu_selesai"]):
                        raise JadwalInstrumenBentrokError(f"Instrumen {id_inst} sudah dipakai pada jam tersebut!")

            # 3. Jika aman, tambahkan data baru LENGKAP
            proposal_baru = {
                "id_proposal": id_prop,
                "nama_operator": nama_op,
                "id_kubah": id_kubah,
                "id_instrumen": id_inst,
                "waktu_mulai": mulai,
                "waktu_selesai": selesai,
                "target_objek": objek
            }
            jadwal_lama.append(proposal_baru)
            self.db.simpan_json("jadwal_observasi.json", jadwal_lama)
            print(f"SUKSES! Proposal {id_prop} dari operator {nama_op} berhasil dijadwalkan.")
            
        except ValueError:
            print("Error: Input jam harus berupa angka.")
        except JadwalInstrumenBentrokError as e:
            print(f"[DITOLAK - Custom Exception]: {e}")
            
        input("\nTekan Enter untuk kembali...")

    def eksekusi_pengamatan(self):
        print("\n--- SIMULASI PENGAMATAN (SKENARIO CUACA & POLIMORFISME) ---")
        id_inst = input("Pilih ID Instrumen (OPT01/RAD01/KAM01): ").upper()
        
        if id_inst not in self.instrumen_tersedia:
            print("❌ Error: Instrumen tidak ditemukan.")
            return
            
        instrumen = self.instrumen_tersedia[id_inst]
        
        print(f"\n--- Kalibrasi Lingkungan untuk {instrumen.nama_instrumen} ---")
        cuaca = input("Kondisi Cuaca (Cerah/Berawan/Hujan/Badai Petir): ")
        fase_bulan = input("Fase Bulan (Purnama/Sabit/Baru dll): ")
        
        try:
            elevasi = float(input("Elevasi Target (0-90 derajat): "))
            
            # --- POLYMORPHISM IN ACTION ---
            if instrumen.hitung_kelayakan_pengamatan(cuaca, elevasi, fase_bulan):
                print(f"\n STATUS: AMAN! Observasi menggunakan {instrumen.nama_instrumen} dapat dilaksanakan.")
                
        except ValueError:
             print("❌ Error: Elevasi harus berupa angka.")
        except CuacaTidakLayakError as e:
             print(f"\n❌ [OBSERVASI DIBATALKAN - Custom Exception]: {e}")
             
        input("\nTekan Enter untuk kembali...")

    def cetak_laporan(self):
        print("\n--- CETAK LAPORAN (STRATEGY PATTERN) ---")
        jadwal = self.db.baca_json("jadwal_observasi.json")
        
        if not jadwal:
            print("⚠️ Jadwal masih kosong. Belum ada yang bisa dicetak.")
        else:
            # Mengekspor dalam dua format sekaligus secara dinamis
            self.laporan_txt.buat_laporan(jadwal, "data/laporan_pengamatan.txt")
            self.laporan_csv.buat_laporan(jadwal, "data/hasil_pengamatan.csv")
            print("SUKSES! File 'laporan_pengamatan.txt' dan 'hasil_pengamatan.csv' berhasil dibuat di folder 'data/'.")
            
        input("\nTekan Enter untuk kembali...")