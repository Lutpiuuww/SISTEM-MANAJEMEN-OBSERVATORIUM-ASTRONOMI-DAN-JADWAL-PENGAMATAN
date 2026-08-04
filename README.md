🔭 OBSERVA - Sistem Manajemen Observatorium Astronomi & Jadwal Pengamatan
Selamat datang di repositori resmi OBSERVA (Sistem Manajemen Observatorium Astronomi dan Jadwal Pengamatan). Ini adalah platform full-stack modern yang dirancang untuk mengelola operasional fasilitas astronomi, mengotomatiskan antrean jadwal observasi teleskop utama, dan menyediakan visualisasi live 3D holografik serta pemantauan cuaca real-time.

Aplikasi ini menggabungkan antarmuka web futuristik (Next.js) dengan mesin rendering 3D WebGL (React Three Fiber/Three.js) dan server API yang cepat (FastAPI) untuk memberikan pengalaman operasi observatorium kelas profesional yang "Pro Max".

🚀 1. Penjelasan Program
OBSERVA bertujuan untuk memecahkan tantangan kompleks dalam manajemen jadwal pengamatan astronomi. Sistem ini bertindak sebagai jembatan antara operator observatorium, data jadwal observasi, dan teleskop fisik (atau simulasi teleskop).

Berikut adalah modul-modul utama dan fungsinya:

🖥️ A. Dashboard Utama (Command Center)
Modul ini adalah layar pemantauan langsung yang menampilkan:

Indikator Server Online: Memantau status koneksi ke server API Backend.

Tabel Jadwal Terdaftar: Daftar antrean jadwal pengamatan yang sedang aktif, dibaca dari Local Storage dan/atau API.

Popup Tangkapan Lensa Teleskop Realistis: Fitur unggulan di mana pengguna dapat mengklik tombol "BIDIK OBJEK" pada jadwal untuk membuka popup kaca transparan yang proyeksikan visualisasi 3D realistis dari objek target yang berputar perlahan dengan latar belakang bintang-bintang 3D, lengkap dengan efek korona Matahari dan pola pita gas raksasa Jupiter yang stilis.

📅 B. Manajemen Jadwal (Schedule Manager)
Modul ini berfungsi untuk melihat, mengelola, dan membatalkan jadwal yang telah dibuat:

Floating Scroll Container: Kartu utama memiliki tinggi maksimal yang dibatasi, dan hanya daftarnya saja yang bisa di-scroll menggunakan custom scrollbar transparan ala Pro Max, sehingga tidak mengganggu antarmuka penuh layar.

Fungsi Pembatalan: Tombol hapus merah menyala untuk membatalkan antrean observasi secara instan (tersinkronisasi dengan memori lokal).

🔭 C. Inisiasi Observasi (Initiate Observation)
Modul ini adalah panel kontrol utama untuk operator:

Formulir Input Kaca: Operator dapat menginisiasi observasi baru dengan memasukkan ID Proposal, Nama Objek Target (misal: "Nebula Orion"), Jam Mulai, Jam Selesai, Instrumen, dan Cuaca Simulasi.

Tombol "Inisiasi Pengamatan": Memproses data, menyimpannya ke memori lokal, dan menambahkan ke antrean jadwal utama.

🌦️ D. Pusat Meteorologi (Meteorology Center)
Modul ini menampilkan simulasi data cuaca kosmik:

Sensor Diagnostik Atmosfer: Kartu-kartu transparan yang menampilkan simulasi Suhu Atmosfer (°C), Kelembapan (%), dan Kecepatan Angin (km/h).

Sinkronisasi Sensor: Tombol untuk mengacak (simulasi pembaruan live) data cuaca dari satelit.

🌌 E. Visualizer 3D Pro Max (3D Holographic Visualizer)
Halaman ini adalah ruang proyeksi 3D utamanya:

Integrasi Jadwal Dinamis: Menu visualizer secara otomatis membaca daftar jadwal yang ada. Jika jadwal baru ditambahkan (misalnya "Nebula Orion" atau "Saturnus"), namanya akan langsung muncul di menu pilihan visualizer ini.

Lensa Pemindai Objek: Area kanvas 3D besar di sebelah kanan yang proyeksikan visualisasi 3D realism (atau hologram kawat) dari objek target yang dipilih.

Pembaruan Visual Realistis: Planet-planet dirender dengan tekstur realistis menggunakan arsip tekstur three.js lama, Matahari memiliki efek emisi bercahaya dan korona, Jupiter memiliki efek pita gas yang stilis, dan Nebula Orion dirender sebagai kumpulan awan gas ungu dan cyan yang menyala (menggunakan teknik sprite dan Additive Blending).

## 📁 2. Struktur Folder Proyek 

Proyek ini menggunakan arsitektur *monorepo* di mana *Backend* Python (dengan pola PBO) dan *Frontend* Next.js berada di dalam satu ruang kerja utama. Berikut adalah pemetaan foldernya:

```text
/
│   # --- PENYIMPANAN DATA LOKAL ---
├── data/                               # Database lokal berbasis JSON
│   ├── hasil_pengamatan...
│   ├── instrumen.json
│   ├── jadwal_observasi.json
│   ├── kubah.json
│   ├── observasi_gagal.json
│   └── operator.json
│
│   # --- BACKEND (PYTHON PBO & FASTAPI) ---
├── src/                                # Sumber kode logika Backend Python
│   ├── cli/                            # Antarmuka Command Line (CLI)
│   │   ├── __init__.py
│   │   └── menu_utama.py
│   ├── core/                           # Logika inti program
│   │   ├── __init__.py
│   │   ├── cuaca_strategy.py           # Pola desain Strategy untuk cuaca
│   │   ├── exceptions.py               # Penanganan error kustom
│   │   └── jadwal_manager.py           # Logika manajemen antrean
│   ├── models/                         # Model data (Entitas)
│   │   ├── instrumen.py
│   │   ├── pengamatan.py
│   │   └── pengguna.py
│   └── utils/                          # Fungsi utilitas bantuan
│       ├── __init__.py
│       └── file_handler.py             # Modul baca/tulis file JSON
│
├── tests/                              # Modul pengujian (Unit testing)
│   ├── __init__.py
│   └── test_observatoriu...
│
├── core_pbo.py                         # File inti Pemrograman Berorientasi Objek
├── strategy_pbo.py                     # Implementasi Design Pattern Strategy
├── main.py                             # Script utama penjalanan backend
├── main_api.py                         # File utama server API Backend (FastAPI)
├── requirements.txt                    # Daftar dependensi Python
│
│   # --- KONFIGURASI FRONTEND (NEXT.JS) ---
├── package.json                        # Dependensi ekosistem Node.js
├── package-lock.json                   # Kunci versi dependensi
├── next.config.ts                      # Konfigurasi inti Next.js
├── tsconfig.json                       # Konfigurasi TypeScript
├── postcss.config.mjs                  # Konfigurasi pemrosesan CSS
├── eslint.config.mjs                   # Aturan linter penulisan kode
├── next-env.d.ts                       # Tipe data environment Next.js
├── .gitignore                          # Pengecualian file untuk Git
├── README.md                           # Dokumentasi proyek (File ini)


│
│   # --- ANTARMUKA FRONTEND (UI) ---
├── frontend-observatorium/             # Folder UI (User Interface)
│   ├── .next/                          # Folder build hasil kompilasi Next.js
│   ├── node_modules/                   # Pustaka instalasi Node.js lokal
│   ├── public/                         # Folder aset statis (Gambar/Tekstur 3D)
│   └── src/                            # Sumber kode Frontend (React/Next.js)
│       ├── app/                        # Sistem App Router Next.js
│       │   ├── cuaca/                  # Halaman Pusat Meteorologi
│       │   ├── jadwal/                 # Halaman Manajemen Jadwal
│       │   ├── observasi/              # Halaman Inisiasi Observasi
│       │   ├── visualizer/             # Halaman Visualizer 3D Pro Max
│       │   ├── favicon.ico             # Ikon web
│       │   ├── globals.css             # Konfigurasi gaya Tailwind CSS
│       │   ├── layout.tsx              # Tata letak global & Latar Belakang 3D
│       │   └── page.tsx                # Halaman Dashboard Utama
│       └── components/                 # Komponen UI modular yang dapat digunakan ulang
│           └── Sidebar.tsx             # Navigasi Menu Kaca Transparan
│
Penjelasan Detail Folder Utama:
/ (Root): Folder paling luar yang menampung server API Backend (main_api.py) dan dokumentasi utama.

frontend-observatorium/src/app/: Lokasi sistem App Router Next.js. Setiap sub-folder di dalamnya mewakili satu rute URL di aplikasi web Anda.

frontend-observatorium/public/: Folder yang wajib digunakan untuk menyimpan aset gambar Nebula secara lokal, agar dapat dipanggil dengan aman tanpa error CORS.

🛠️ 3. Panduan Instalasi (Langkah demi Langkah Tanpa Terlewat)
Ikuti panduan ini dari awal sampai akhir untuk mengonfigurasi dan menjalankan sistem OBSERVA di komputer lokal Anda:

Prasyarat Sistem:
Sebelum memulai, pastikan Anda telah menginstal:

Node.js & npm (v18 ke atas) - Unduh di sini.

Python (v3.8 ke atas) - Unduh di sini.

(Opsional) Git - Unduh di sini.

Langkah 1: Kloning atau Membuat Folder Proyek
Jika Anda menggunakan Git:

Bash
git clone https://github.com/username/obsereva.git
Atau jika Anda membangunnya dari nol, buat folder baru dan pastikan struktur folder di atas telah Anda replikasi (terutama folder frontend-observatorium di dalamnya).

Bagian I: Konfigurasi Backend (API Server)
Langkah 2: Instalasi Dependensi Python
Buka terminal baru di folder utama (root) proyek Anda:

Bash
# Instal dependensi backend Python
pip install fastapi uvicorn pydantic
(Catatan: Anda bisa menambahkan pustaka lain ke requirements.txt dan menginstalnya dengan pip install -r requirements.txt)

Bagian II: Konfigurasi Frontend (Next.js)
Langkah 3: Menyiapkan Aset Foto Nebula (Sangat Penting)
Untuk memastikan visualisasi Nebula Orion berfungsi tanpa error, Anda wajib menggunakan foto Nebula Anda sendiri secara lokal:

Cari file foto image_28e2bc.jpg (atau nama lainnya) milik Anda.

Pindahkan atau salin file tersebut ke dalam folder frontend-observatorium/public/.

Pastikan nama filenya diubah menjadi image_28e2bc.jpg (agar sesuai dengan kode).

Langkah 4: Instalasi Dependensi Node.js
Buka terminal baru dan arahkan ke dalam folder frontend:

Bash
cd frontend-observatorium

# Instal dependensi frontend (membaca dari package.json)
npm install
Daftar paket utama yang akan diinstal meliputi:

next, react, react-dom (Next.js)

tailwindcss, postcss, autoprefixer (Tailwind)

lucide-react (Ikon)

@react-three/fiber, @react-three/drei, three (Mesin Rendering 3D Pro Max)

💻 4. Menjalankan Program (Dari Awal Sampai Akhir)
Setelah semua dependensi terinstal, ikuti langkah ini untuk menjalankan sistem OBSERVA lengkap:

Langkah 1: Menjalankan Server API Backend
Buka terminal baru di folder utama (root) proyek Anda:

Bash
# Jalankan server FastAPI dengan Uvicorn
uvicorn main_api:app --reload --port 8000
Server API Backend akan berjalan di [http://127.0.0.1:8000](http://127.0.0.1:8000)

Langkah 2: Menjalankan Server Pengembangan Frontend
Buka terminal baru yang berbeda dan arahkan ke dalam folder frontend:

Bash
cd frontend-observatorium

# Jalankan server pengembangan Next.js
npm run dev
Aplikasi web frontend dapat diakses melalui http://localhost:3000

Cara Mengetes Sistem Lengkap:
Akses http://localhost:3000 di browser Anda.

Pergi ke menu "Inisiasi Observasi" dan masukkan data baru (misalnya objek: "Nebula Orion").

Pergi ke Dashboard. Data baru akan muncul di tabel. Klik tombol "BIDIK OBJEK" untuk melihat popup Lensa Teleskop Realistis Nebula Orion yang menyala!

Pergi ke "Manajemen Jadwal" untuk mengontrol antrean.

Pergi ke "Visualizer 3D Pro Max". Menu dinamis di sebelah kiri akan secara otomatis memuat target jadwal observasi Anda, dan Anda bisa memindainya secara real-time di kanvas 3D!

🏆 5. Detail Teknis Pro Max (Catatan Pengembangan)
Sistem ini menggunakan teknik-teknik canggih berikut untuk mencapai kualitas visual dan kinerja tingkat profesional:

Teknik Rendering 3D (WebGL/Three.js):
Matahari Membara: Menggunakan meshStandardMaterial dengan efek emisi (emissive Intensity={1.5}) dan material AdditiveBlending tembus pandang untuk korona/halo.

Pita Gas Jupiter: Menggunakan teknik manipulasi tekstur di mana tekstur Bulan diregangkan secara horizontal (repeat.set(1, 4)) dan diberi warna cokelat Jupiter.

Nebula Orion (Additive Blending): Menggunakan teknik Sprite dengan material yang memakai THREE.AdditiveBlending. Latar belakang hitam pada foto Nebula otomatis melebur sempurna dengan bintang-bintang di sekitarnya, menghasilkan hamburan awan debu ungu dan cyan kosmik yang megah seperti tangkapan teleskop Hubble asli!

Desain Antarmuka (Glassmorphism & AMOLED Dark):
Aura Obsidian: Menggunakan warna dasar Obsidian Gelap (bg-[#0a0d16]/80) untuk kontras tajam ala AMOLED.

Garis Tepi Ungu: Menggunakan garis tepi tipis dan pendaran aura kosmik berwarna ungu gelap (border-purple-500/20 dan efek shadow) untuk kemewahan yang konsisten di semua halaman.

Integrasi Frontend/Backend:
Manajemen Status Lokal: Sinkronisasi jadwal antara Inisiasi, Dashboard, dan Visualizer menggunakan memori lokal dan/atau API FastAPI.

👨‍💻 6. Pengembang & Penafian
Pengembang Utama:
Muhammad Luthfi Fadil
250180089

Program Studi Sistem Informasi, Universitas Malikussaleh

Penafian:
Proyek ini dirancang sebagai purwarupa (prototype) sistem kontrol fasilitas astronomi tingkat lanjut. Data yang ditampilkan adalah simulasi dan arsitektur visualnya dirancang untuk kepentingan demonstrasi teknologi dan kemewahan antarmuka kosmik.