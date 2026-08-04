# 🔭 OBSERVA - Frontend (Next.js UI)

Antarmuka pengguna (*User Interface*) berbasis web untuk sistem manajemen observatorium astronomi **OBSERVA**, dibangun dengan teknologi modern untuk memberikan pengalaman kontrol fasilitas kosmik bergaya *Pro Max*.

## 🚀 Fitur Antarmuka
*   **Dashboard Utama (Command Center):** Pemantauan status server dan tabel jadwal observasi interaktif lengkap dengan fitur **"Bidik Objek"** yang membuka *popup* tangkapan lensa teleskop 3D real-time.
*   **Manajemen Jadwal:** Kontrol antrean pengamatan dengan kontainer gulir mengambang (*floating scroll*) dan akses pembatalan instan.
*   **Inisiasi Observasi:** Panel formulir input data untuk menjadwalkan target pengamatan baru ke dalam sistem.
*   **Pusat Meteorologi:** Dasbor diagnostik atmosfer untuk memantau suhu, kelembapan, dan kecepatan angin dengan tombol sinkronisasi satelit.
*   **Visualizer 3D Pro Max:** Ruang proyeksi holografik berbasis WebGL menggunakan *React Three Fiber* yang membaca data jadwal secara dinamis, menampilkan tekstur planet realistis, Matahari bercahaya, pita gas Jupiter, hingga Nebula Orion berbasis *Sprite Additive Blending*.

## 🛠️ Tumpukan Teknologi (Tech Stack)
*   **Framework:** Next.js (App Router)
*   **Bahasa Pemrograman:** TypeScript / JavaScript (React)
*   **Penataan Gaya (Styling):** Tailwind CSS (Glassmorphism & AMOLED Dark Theme)
*   **Mesin Render 3D:** Three.js, @react-three/fiber, @react-three/drei
*   **Pustaka Ikon:** Lucide React

## 📁 Struktur Direktori Frontend
```text
frontend-observatorium/
├── public/                 # Aset statis (termasuk foto lokal image_28e2bc.jpg untuk Nebula)
├── src/
│   ├── app/                # Sistem App Router Next.js
│   │   ├── cuaca/          # Halaman Pusat Meteorologi
│   │   ├── jadwal/         # Halaman Manajemen Jadwal
│   │   ├── observasi/      # Halaman Inisiasi Observasi
│   │   ├── visualizer/     # Halaman Visualizer 3D Pro Max
│   │   ├── globals.css     # Pengaturan gaya global Tailwind
│   │   ├── layout.tsx      # Tata letak global & Latar Belakang Galaksi 3D
│   │   └── page.tsx        # Halaman Dashboard Utama
│   └── components/         # Komponen modular
│       └── Sidebar.tsx     # Bilah navigasi samping dengan menu dinamis
├── package.json            # Daftar dependensi Node.js
├── next.config.ts          # Konfigurasi inti Next.js
└── tsconfig.json           # Konfigurasi TypeScript

Panduan Menjalankan Frontend
Pastikan Anda berada di dalam folder frontend-observatorium:

Bash
cd frontend-observatorium
Instal seluruh pustaka dan dependensi yang dibutuhkan:

Bash
npm install
Pastikan aset gambar lokal (seperti image_28e2bc.jpg untuk tekstur Nebula) sudah berada di dalam folder public/.

Jalankan server pengembangan lokal:

Bash
npm run dev
Akses aplikasi melalui peramban web pada tautan http://localhost:3000.