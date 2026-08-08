"use client";
import { useState, useEffect } from "react";
import { CalendarDays, Trash2, AlertCircle } from "lucide-react";

export default function JadwalPage() {
  const [jadwal, setJadwal] = useState<any[]>([]);

  // FUNGSI MENGAMBIL DATA DARI BACKEND
  const fetchJadwal = async () => {
    try {
      const response = await fetch("backend-observa.vercel.app", {
        cache: "no-store" // <-- Memastikan data selalu segar (tidak di-cache)
      });
      if (response.ok) {
        const data = await response.json();
        setJadwal(data.reverse());
      }
    } catch (error) {
      console.error("Gagal mengambil data dari server:", error);
    }
  };

  useEffect(() => {
    fetchJadwal();
  }, []);

  // FUNGSI MENGHAPUS DATA KE BACKEND
  const handleHapus = async (id_proposal: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/jadwal/${id_proposal}`, {
        method: "DELETE",
      });
      
      if (response.ok) {
        fetchJadwal(); // Ambil ulang data terbaru setelah berhasil dihapus
      } else {
        alert("Gagal membatalkan jadwal di server.");
      }
    } catch (error) {
      console.error("Error menghapus jadwal:", error);
    }
  };

  return (
    <div className="w-full min-h-screen p-10 flex flex-col items-center justify-center overflow-x-hidden relative bg-transparent">
      
      <div className="w-full max-w-3xl max-h-[75vh] flex flex-col bg-[#0a0d16]/10 backdrop-blur-md border border-white/10 rounded-3xl p-6 shadow-[0_0_30px_rgba(168,85,247,0.15)] relative z-10">
        
        <div className="flex items-center gap-4 mb-6 border-b border-white/10 pb-6 shrink-0">
          <div className="w-12 h-12 rounded-xl bg-emerald-500/20 flex items-center justify-center border border-emerald-500/30">
            <CalendarDays className="text-emerald-400" size={28} />
          </div>
          <div>
            <h1 className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 tracking-wide">
              MANAJEMEN JADWAL
            </h1>
            <p className="text-xs text-gray-400 tracking-widest font-mono mt-1 uppercase">
              Kontrol Antrean & Akses Pembatalan
            </p>
          </div>
        </div>

        <div className="space-y-4 overflow-y-auto pr-4 [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar-track]:bg-transparent [&::-webkit-scrollbar-thumb]:bg-purple-500/30 hover:[&::-webkit-scrollbar-thumb]:bg-purple-500/50 [&::-webkit-scrollbar-thumb]:rounded-full">
          {jadwal.length === 0 ? (
            <div className="bg-black/40 border border-white/5 rounded-2xl p-10 text-center flex flex-col items-center justify-center backdrop-blur-md">
              <AlertCircle className="text-gray-500 mb-3" size={40} />
              <p className="text-gray-400 font-mono text-sm">Tidak ada jadwal observasi yang aktif.</p>
            </div>
          ) : (
            jadwal.map((item, index) => (
              <div key={index} className="bg-[#03050a]/60 border border-white/5 hover:border-emerald-500/30 transition-all rounded-2xl p-5 flex items-center justify-between backdrop-blur-md group">
                <div className="flex items-center gap-6">
                  <div className="text-center px-4 border-r border-white/10">
                    <span className="block text-xl font-black text-emerald-400">{item.jam_mulai}:00</span>
                    <span className="text-[10px] text-gray-500 font-mono tracking-widest uppercase">Waktu Mulai</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-white">{item.target_objek}</h3>
                    <p className="text-xs text-gray-400 flex gap-3 mt-1">
                      <span>Proposal: <span className="text-purple-400 font-mono">{item.id_proposal}</span></span>
                      <span>Instrumen: <span className="text-cyan-400">{item.instrumen}</span></span>
                    </p>
                  </div>
                </div>
                
                <button 
                  onClick={() => handleHapus(item.id_proposal)} // Menggunakan id_proposal
                  className="w-10 h-10 rounded-full bg-red-500/10 hover:bg-red-500 border border-transparent hover:border-red-500 text-red-500 hover:text-white flex items-center justify-center transition-all shadow-[0_0_15px_rgba(239,68,68,0)] hover:shadow-[0_0_20px_rgba(239,68,68,0.5)]"
                  title="Batalkan Sesi"
                >
                  <Trash2 size={18} />
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}