"use client";
import { useState } from "react";
import { Telescope, Loader2, CheckCircle2, X, AlertTriangle } from "lucide-react";

export default function ObservasiPage() {
  const initialFormState = {
    id_proposal: "",
    target_objek: "",
    jam_mulai: "",
    jam_selesai: "",
    instrumen: "Teleskop Optik",
    cuaca: "Cerah"
  };

  const [formData, setFormData] = useState(initialFormState);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  
  // State baru untuk menangani Modal Error Kosmik
  const [errorMessage, setErrorMessage] = useState("");
  const [showErrorModal, setShowErrorModal] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      const response = await fetch("http://localhost:8000/api/jadwal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        // Tangkap pesan error dari FastAPI (JadwalBentrokError) dan tampilkan di Modal Error
        setErrorMessage(errorData.detail || "Terjadi kesalahan pada sistem.");
        setShowErrorModal(true);
        setIsSubmitting(false);
        return;
      }

      setShowSuccessModal(true);
      setFormData(initialFormState);
      
    } catch (error) {
      console.error("Gagal menghubungi server", error);
      setErrorMessage("Koneksi gagal! Pastikan server FastAPI (Backend) sedang berjalan di port 8000.");
      setShowErrorModal(true);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="w-full min-h-screen p-10 flex flex-col items-center justify-center overflow-x-hidden relative bg-transparent">
      
      {/* Efek Pendaran Latar Belakang */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-emerald-600/10 rounded-full blur-[120px] pointer-events-none"></div>

      {/* Kartu Formulir Utama */}
      <div className="w-full max-w-4xl bg-[#0a0d16]/10 backdrop-blur-md border border-white/10 rounded-3xl p-8 shadow-[0_0_30px_rgba(168,85,247,0.15)] relative z-10">
        
        <div className="flex items-center gap-4 mb-8 border-b border-white/5 pb-6">
          <div className="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center border border-purple-500/50">
            <Telescope className="text-purple-400" size={28} />
          </div>
          <div>
            <h1 className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 tracking-wide">
              SISTEM OBSERVATORIUM
            </h1>
            <p className="text-xs text-purple-400 tracking-widest font-mono font-bold mt-1 uppercase">
              Panel Kendali Teleskop Utama
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">ID Proposal</label>
            <input type="text" name="id_proposal" value={formData.id_proposal} onChange={handleChange} className="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-gray-300 focus:outline-none focus:border-purple-500 transition-colors" required />
          </div>
          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Target Objek</label>
            <input type="text" name="target_objek" value={formData.target_objek} onChange={handleChange} className="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-gray-300 focus:outline-none focus:border-purple-500 transition-colors" required />
          </div>
          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Jam Mulai (0-23)</label>
            <input type="number" name="jam_mulai" value={formData.jam_mulai} onChange={handleChange} className="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-gray-300 focus:outline-none focus:border-purple-500 transition-colors" required />
          </div>
          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Jam Selesai (0-23)</label>
            <input type="number" name="jam_selesai" value={formData.jam_selesai} onChange={handleChange} className="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-gray-300 focus:outline-none focus:border-purple-500 transition-colors" required />
          </div>
          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Instrumen</label>
            <select name="instrumen" value={formData.instrumen} onChange={handleChange} className="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-gray-300 focus:outline-none focus:border-purple-500 transition-colors appearance-none">
              <option value="Teleskop Optik">Teleskop Optik</option>
              <option value="Teleskop Radio">Teleskop Radio</option>
            </select>
          </div>
          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Cuaca Simulasi</label>
            <select name="cuaca" value={formData.cuaca} onChange={handleChange} className="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-gray-300 focus:outline-none focus:border-purple-500 transition-colors appearance-none">
              <option value="Cerah">Cerah (Clear)</option>
              <option value="Berawan">Berawan (Cloudy)</option>
              <option value="Hujan">Hujan (Rain)</option>
              <option value="Badai Petir">Badai (Storm)</option>
            </select>
          </div>
        </div>

        <button 
          onClick={handleSubmit}
          disabled={isSubmitting}
          className={`w-full mt-8 font-black py-4 rounded-xl transition-all uppercase tracking-widest flex items-center justify-center gap-2
            ${isSubmitting 
              ? "bg-gray-600 text-gray-400 cursor-not-allowed" 
              : "bg-gradient-to-r from-emerald-500 to-emerald-400 hover:from-emerald-400 hover:to-emerald-300 text-black shadow-[0_0_20px_rgba(16,185,129,0.4)] hover:scale-[1.02] active:scale-95"
            }`}
        >
          {isSubmitting ? (
            <>
              <Loader2 className="animate-spin" size={20} />
              MENGINISIASI...
            </>
          ) : (
            "Inisiasi Pengamatan"
          )}
        </button>
      </div>

      {/* MODAL NOTIFIKASI SUKSES */}
      {showSuccessModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm px-4">
          <div className="bg-[#050810] border border-emerald-500/30 rounded-2xl p-8 max-w-sm w-full shadow-[0_0_50px_rgba(16,185,129,0.2)] relative animate-in fade-in zoom-in duration-300">
            <button 
              onClick={() => setShowSuccessModal(false)}
              className="absolute top-4 right-4 text-gray-500 hover:text-white transition-colors"
            >
              <X size={20} />
            </button>
            <div className="flex flex-col items-center text-center mt-2">
              <div className="w-16 h-16 rounded-full bg-emerald-500/20 flex items-center justify-center mb-6 border border-emerald-500/50 shadow-[0_0_20px_rgba(16,185,129,0.4)]">
                <CheckCircle2 className="text-emerald-400" size={32} />
              </div>
              <h2 className="text-xl font-black text-white mb-2 tracking-wide">KODE DITERIMA</h2>
              <p className="text-sm text-gray-400 mb-6 leading-relaxed">
                Proposal <span className="text-emerald-400 font-bold">{formData.id_proposal || "Baru"}</span> telah divalidasi. Menunggu kalibrasi teleskop untuk target <span className="text-purple-400 font-bold">{formData.target_objek}</span>.
              </p>
              <button 
                onClick={() => setShowSuccessModal(false)}
                className="w-full bg-white/5 hover:bg-white/10 border border-white/10 text-white font-bold py-3 rounded-xl transition-all"
              >
                Tutup Panel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL NOTIFIKASI ERROR (RED ALERT KOSMIK) */}
      {showErrorModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-md px-4">
          <div className="bg-[#0c0508] border border-red-500/40 rounded-2xl p-8 max-w-md w-full shadow-[0_0_60px_rgba(239,68,68,0.25)] relative animate-in fade-in zoom-in duration-300">
            <button 
              onClick={() => setShowErrorModal(false)}
              className="absolute top-4 right-4 text-gray-500 hover:text-white transition-colors"
            >
              <X size={20} />
            </button>
            <div className="flex flex-col items-center text-center mt-2">
              <div className="w-16 h-16 rounded-full bg-red-500/20 flex items-center justify-center mb-6 border border-red-500/50 shadow-[0_0_25px_rgba(239,68,68,0.4)]">
                <AlertTriangle className="text-red-400 animate-pulse" size={32} />
              </div>
              
              <h2 className="text-xl font-black text-red-400 mb-2 tracking-wide uppercase">Peringatan Sistem</h2>
              <p className="text-sm text-gray-300 mb-6 leading-relaxed bg-red-950/20 border border-red-500/20 rounded-xl p-4">
                {errorMessage}
              </p>
              <button 
                onClick={() => setShowErrorModal(false)}
                className="w-full bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 text-red-300 font-bold py-3 rounded-xl transition-all shadow-[0_0_15px_rgba(239,68,68,0.2)]"
              >
                Mengerti & Kembali
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}