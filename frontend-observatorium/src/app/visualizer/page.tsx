"use client";
import { useState, useEffect, Suspense, useMemo } from "react";
import { Globe, Info, Orbit, Crosshair, AlertCircle } from "lucide-react";
import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls, Stars, Html, useProgress } from "@react-three/drei";
import * as THREE from "three";

// 1. Fungsi Dinamis Penghasil Info Objek
const getPlanetData = (targetName: string) => {
  const name = targetName.toLowerCase();
  if (name.includes("bumi") || name.includes("earth")) {
    return { desc: "Planet ketiga dari Matahari. Biosfer aktif, tingkat kelembapan stabil.", status: "AMAN (Kondisi Ideal)", theme: "emerald" };
  }
  if (name.includes("mars")) {
    return { desc: "Planet merah. Terdeteksi aktivitas badai debu di ekuator utara.", status: "PERINGATAN (Badai Permukaan)", theme: "red" };
  }
  if (name.includes("jupiter")) {
    return { desc: "Raksasa gas dengan pola pita awan badai amonia yang kuat.", status: "STABIL (Radiasi Tinggi)", theme: "orange" };
  }
  if (name.includes("matahari") || name.includes("sun")) {
    return { desc: "Bintang deret utama tipe G. Aktivitas jilatan api (solar flare) terpantau.", status: "AWAS (Panas Ekstrem)", theme: "yellow" };
  }
  // Default untuk objek acak yang diinput user (misal: Nebula, Komet, Asteroid)
  return { desc: `Objek angkasa terdaftar: ${targetName}. Sistem sedang melakukan kalibrasi spektrum lanjutan.`, status: "MEMINDAI...", theme: "cyan" };
};

// 2. Komponen Loading
function Loader() {
  const { progress } = useProgress();
  return (
    <Html center>
      <span className="text-emerald-400 font-mono text-xs tracking-widest bg-black/80 px-4 py-2 rounded-full border border-emerald-500/30 whitespace-nowrap">
        MEMUAT TEKSTUR {progress.toFixed(0)}%
      </span>
    </Html>
  );
}

// 3. Komponen Render Planet Realistis (Visualizer Edition)
function RealisticPlanet({ target }: { target: string }) {
  const targetLower = target.toLowerCase();
  
  // 1. MATAHARI (Bola Pijar + Korona)
  if (targetLower.includes("matahari") || targetLower.includes("sun")) {
    return (
      <group>
        <mesh>
          <sphereGeometry args={[2.3, 64, 64]} />
          <meshStandardMaterial color="#fbbf24" emissive="#ea580c" emissiveIntensity={1.5} />
        </mesh>
        <mesh>
          <sphereGeometry args={[2.5, 64, 64]} />
          <meshBasicMaterial color="#f97316" transparent opacity={0.2} blending={THREE.AdditiveBlending} />
        </mesh>
      </group>
    );
  }

  // 2. NEBULA (REALISTIS 100% FOTO ASLI)
  if (targetLower.includes("nebula") || targetLower.includes("awan")) {
      
      // Memanggil gambar langsung dari folder "public" milikmu! Bebas dari blokir internet (CORS).
      const nebulaTex = useLoader(THREE.TextureLoader, "/nebula.jpg");
      
      return (
        <sprite scale={[12, 12, 1]}>
          <spriteMaterial 
            map={nebulaTex} 
            transparent 
            blending={THREE.AdditiveBlending} 
            opacity={1} 
          />
        </sprite>
      );
    }

  // 3. PLANET SOLID (Bumi, Mars, Jupiter, dll)
  let textureUrl = "https://raw.githubusercontent.com/mrdoob/three.js/r128/examples/textures/planets/earth_atmos_2048.jpg";
  let planetColor = "#ffffff"; 

  if (targetLower.includes("mars")) {
    textureUrl = "https://raw.githubusercontent.com/mrdoob/three.js/r128/examples/textures/planets/moon_1024.jpg";
    planetColor = "#ef4444"; 
  } else if (targetLower.includes("jupiter")) {
    textureUrl = "https://raw.githubusercontent.com/mrdoob/three.js/r128/examples/textures/planets/moon_1024.jpg";
    planetColor = "#d9a066";
  } else if (!targetLower.includes("bumi") && !targetLower.includes("earth")) {
    textureUrl = "https://raw.githubusercontent.com/mrdoob/three.js/r128/examples/textures/planets/moon_1024.jpg";
    planetColor = "#9ca3af"; // Tekstur bulan abu-abu untuk objek acak lainnya
  }

  const texture = useLoader(THREE.TextureLoader, textureUrl);
  
  if (targetLower.includes("jupiter")) {
    const tex = texture.clone();
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(1, 4); // Regangkan untuk membentuk pita gas Jupiter
    tex.needsUpdate = true;
    return (
      <mesh>
        <sphereGeometry args={[2.5, 64, 64]} />
        <meshStandardMaterial map={tex} color={planetColor} roughness={0.8} metalness={0.1} />
      </mesh>
    );
  }
  
  return (
    <mesh>
      <sphereGeometry args={[2.5, 64, 64]} />
      <meshStandardMaterial map={texture} color={planetColor} roughness={0.8} metalness={0.1} />
    </mesh>
  );
}

export default function VisualizerPage() {
  const [jadwalTargets, setJadwalTargets] = useState<string[]>([]);
  const [selected, setSelected] = useState<string | null>(null);

  // Mengambil Data dari Dashboard/Inisiasi saat halaman dibuka
  useEffect(() => {
    const savedData = JSON.parse(localStorage.getItem("jadwal_observasi") || "[]");
    // Mengekstrak hanya nama objeknya (Bumi, Mars, Jupiter, dsb)
    const targets = savedData.map((item: any) => item.target_objek);
    // Menyaring agar tidak ada nama planet yang duplikat
    const uniqueTargets = Array.from(new Set(targets)) as string[];
    
    setJadwalTargets(uniqueTargets);
    
    // Auto-pilih planet pertama jika ada data
    if (uniqueTargets.length > 0) {
      setSelected(uniqueTargets[0]);
    }
  }, []);

  const activeData = selected ? getPlanetData(selected) : null;

  return (
    <div className="w-full min-h-screen p-10 flex flex-col items-center justify-center overflow-x-hidden relative bg-transparent">
      
      <div className="w-full max-w-6xl h-[80vh] flex gap-6 relative z-10">
        
        {/* PANEL KIRI: Menu Pilihan Dinamis */}
        <div className="w-1/3 h-full bg-[#0a0d16]/10 backdrop-blur-md border border-white/10 rounded-3xl p-8 flex flex-col shadow-[0_0_30px_rgba(168,85,247,0.15)]">
          <div className="flex items-center gap-3 mb-8 border-b border-white/10 pb-6">
            <Orbit className="text-purple-400 animate-spin-slow" size={28} />
            <div>
              <h2 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400 tracking-wide">
                VISUALIZER 3D
              </h2>
              <p className="text-xs text-gray-400 tracking-widest font-mono uppercase">Lensa Pemindai Objek</p>
            </div>
          </div>

          {/* Render List berdasarkan Jadwal */}
          {jadwalTargets.length === 0 ? (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-6 border border-dashed border-white/10 rounded-2xl bg-black/20">
              <AlertCircle className="text-gray-500 mb-4" size={40} />
              <p className="text-sm text-gray-400 font-bold mb-1">DATA KOSONG</p>
              <p className="text-xs text-gray-500">Silakan inisiasi observasi target di menu Inisiasi terlebih dahulu.</p>
            </div>
          ) : (
            <div className="flex-1 space-y-3 overflow-y-auto pr-2">
              {jadwalTargets.map((planet) => (
                <button
                  key={planet}
                  onClick={() => setSelected(planet)}
                  className={`w-full text-left px-5 py-4 rounded-xl flex items-center justify-between transition-all font-bold tracking-widest uppercase text-sm ${
                    selected === planet
                      ? "bg-purple-500/20 text-purple-300 border border-purple-500/50 shadow-[0_0_15px_rgba(168,85,247,0.3)]"
                      : "bg-black/40 text-gray-400 border border-white/5 hover:border-purple-500/30 hover:bg-white/5"
                  }`}
                >
                  {planet}
                  {selected === planet && <Crosshair size={16} className="animate-pulse" />}
                </button>
              ))}
            </div>
          )}

          {/* Info Status Panel Bawah */}
          {activeData && (
            <div className="mt-4 p-5 bg-black/50 border border-white/10 rounded-2xl animate-in fade-in duration-300">
              <div className="flex items-start gap-3">
                <Info className="text-cyan-400 shrink-0 mt-0.5" size={18} />
                <div>
                  <span className="text-[10px] text-gray-500 font-mono tracking-widest uppercase block mb-1">Diagnostik Target</span>
                  <p className="text-xs text-gray-300 leading-relaxed">{activeData.desc}</p>
                  <div className={`mt-3 text-[10px] font-black tracking-widest px-3 py-1 bg-${activeData.theme}-500/10 inline-block rounded-md text-${activeData.theme}-400 border border-${activeData.theme}-500/30`}>
                    {activeData.status}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* PANEL KANAN: Kanvas 3D Realistis */}
        <div className="flex-1 h-full bg-[#0a0d16]/10 backdrop-blur-md border border-white/10 rounded-3xl relative overflow-hidden shadow-[0_0_30px_rgba(168,85,247,0.15)] cursor-move">
          
          {selected ? (
            <>
              <div className="absolute top-6 left-6 z-20 flex items-center gap-3">
                <div className="w-3 h-3 rounded-full bg-red-500 animate-pulse"></div>
                <span className="font-mono text-xs text-white tracking-widest bg-black/60 px-4 py-2 rounded-full border border-white/10 uppercase">
                  TARGET TERKUNCI: {selected}
                </span>
              </div>
              <div className="absolute bottom-6 right-6 z-20">
                 <span className="font-mono text-[10px] text-gray-500 uppercase tracking-widest bg-black/40 px-3 py-1 rounded-full">
                   [Gunakan Mouse Untuk Memutar & Zoom]
                 </span>
              </div>

              <div className="absolute inset-0 pointer-events-none z-10 flex items-center justify-center">
                 <div className="w-full h-[1px] bg-emerald-500/20 absolute"></div>
                 <div className="h-full w-[1px] bg-emerald-500/20 absolute"></div>
                 <div className="w-96 h-96 border border-emerald-500/20 rounded-full absolute"></div>
              </div>

              <Canvas camera={{ position: [0, 0, 6] }}>
                <ambientLight intensity={0.05} />
                <directionalLight position={[5, 3, 5]} intensity={2} color="#ffffff" />
                
                <Stars radius={100} depth={50} count={3000} factor={3} saturation={0} fade speed={1} />
                
                <Suspense fallback={<Loader />}>
                  <RealisticPlanet target={selected} />
                </Suspense>
                
                <OrbitControls autoRotate autoRotateSpeed={1.0} enablePan={false} enableZoom={true} />
              </Canvas>
            </>
          ) : (
             // Tampilan saat tidak ada data sama sekali
             <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/40">
                <Orbit className="text-gray-600 mb-4 animate-spin-slow" size={64} />
                <p className="text-gray-500 font-mono tracking-widest uppercase">VISUALIZER OFFLINE</p>
             </div>
          )}

        </div>

      </div>
    </div>
  );
}