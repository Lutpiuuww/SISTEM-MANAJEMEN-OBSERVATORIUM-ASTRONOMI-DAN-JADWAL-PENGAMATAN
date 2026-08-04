"use client";
import { useState } from "react";
import { CloudLightning, Wind, Droplets, Thermometer, RefreshCw, Satellite } from "lucide-react";

export default function CuacaPage() {
  // State untuk menyimpan data cuaca
  const [cuaca, setCuaca] = useState({ suhu: 18.4, kelembapan: 42, angin: 12 });
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Fungsi simulasi pembaruan data dari satelit
  const handleRefresh = () => {
    setIsRefreshing(true);
    
    // Jeda 1.5 detik untuk efek loading
    setTimeout(() => {
      setCuaca({
        suhu: +(15 + Math.random() * 10).toFixed(1), // Suhu acak antara 15 - 25
        kelembapan: Math.floor(30 + Math.random() * 40), // Kelembapan 30% - 70%
        angin: Math.floor(5 + Math.random() * 25) // Angin 5 - 30 km/h
      });
      setIsRefreshing(false);
    }, 1500);
  };

  return (
    <div className="w-full min-h-screen p-10 flex flex-col items-center justify-center overflow-x-hidden relative bg-transparent">
      
      <div className="w-full max-w-4xl bg-[#0a0d16]/10 backdrop-blur-md border border-white/10 rounded-3xl p-8 shadow-[0_0_30px_rgba(168,85,247,0.15)] relative z-10">
        
        <div className="flex items-center justify-between mb-8 border-b border-white/10 pb-6">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-cyan-500/20 flex items-center justify-center border border-cyan-500/30">
              <CloudLightning className="text-cyan-400" size={28} />
            </div>
            <div>
              <h1 className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400 tracking-wide">
                PUSAT METEOROLOGI
              </h1>
              <p className="text-xs text-gray-400 tracking-widest font-mono mt-1 uppercase">
                Diagnostik Atmosfer & Indeks Cuaca Kubah
              </p>
            </div>
          </div>
          
          <button 
            onClick={handleRefresh}
            disabled={isRefreshing}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-bold text-xs tracking-widest uppercase transition-all ${
              isRefreshing 
                ? "bg-gray-600/50 text-gray-400 cursor-not-allowed border border-gray-500/30" 
                : "bg-cyan-500/20 text-cyan-400 hover:bg-cyan-500/30 border border-cyan-500/50 shadow-[0_0_15px_rgba(6,182,212,0.3)]"
            }`}
          >
            <RefreshCw className={isRefreshing ? "animate-spin" : ""} size={16} />
            {isRefreshing ? "Memindai..." : "Sinkronisasi Sensor"}
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-black/40 border border-white/5 rounded-2xl p-8 flex flex-col items-center justify-center backdrop-blur-md relative overflow-hidden">
            <div className="absolute top-0 w-full h-1 bg-gradient-to-r from-transparent via-emerald-400 to-transparent"></div>
            <Thermometer className="text-emerald-400 mb-4" size={36} />
            <span className="text-xs text-gray-400 block uppercase tracking-widest mb-1">Suhu Atmosfer</span>
            <span className="text-4xl font-black text-white">{cuaca.suhu}°C</span>
          </div>

          <div className="bg-black/40 border border-white/5 rounded-2xl p-8 flex flex-col items-center justify-center backdrop-blur-md relative overflow-hidden">
            <div className="absolute top-0 w-full h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent"></div>
            <Droplets className="text-cyan-400 mb-4" size={36} />
            <span className="text-xs text-gray-400 block uppercase tracking-widest mb-1">Kelembapan</span>
            <span className="text-4xl font-black text-white">{cuaca.kelembapan}%</span>
          </div>

          <div className="bg-black/40 border border-white/5 rounded-2xl p-8 flex flex-col items-center justify-center backdrop-blur-md relative overflow-hidden">
            <div className="absolute top-0 w-full h-1 bg-gradient-to-r from-transparent via-purple-400 to-transparent"></div>
            <Wind className="text-purple-400 mb-4" size={36} />
            <span className="text-xs text-gray-400 block uppercase tracking-widest mb-1">Kec. Angin</span>
            <span className="text-4xl font-black text-white">{cuaca.angin} km/h</span>
          </div>
        </div>

        {/* Indikator Status Tambahan */}
        <div className="mt-6 bg-blue-500/10 border border-blue-500/20 rounded-xl p-4 flex items-center justify-center gap-3 text-blue-400 text-xs font-mono">
          <Satellite size={16} className="animate-pulse" />
          TERHUBUNG DENGAN SATELIT METEOROLOGI GEOSINKRON
        </div>

      </div>
    </div>
  );
}