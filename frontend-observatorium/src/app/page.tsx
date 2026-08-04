"use client";
import { useEffect, useState, Suspense } from "react";
import { Activity, X } from "lucide-react";
import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls, Stars, Html, useProgress } from "@react-three/drei";
import * as THREE from "three";

// 1. Komponen Loading (Saat mengunduh tekstur 3D)
function Loader() {
  const { progress } = useProgress();
  return (
    <Html center>
      <span className="text-emerald-400 font-mono text-xs tracking-widest bg-black/80 px-4 py-2 rounded-full border border-emerald-500/30">
        MEMUAT TEKSTUR {progress.toFixed(0)}%
      </span>
    </Html>
  );
}

// 2. Komponen Render Planet & Nebula (Dashboard Edition)
function RealisticPlanet({ target }: { target: string }) {
  const targetLower = target.toLowerCase();
  
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
  
  if (targetLower.includes("nebula") || targetLower.includes("awan")) {
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
    planetColor = "#9ca3af";
  }
  const texture = useLoader(THREE.TextureLoader, textureUrl);
  
  if (targetLower.includes("jupiter")) {
    const tex = texture.clone();
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(1, 4); 
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

export default function DashboardPage() {
  const [jadwal, setJadwal] = useState<any[]>([]);
  const [telescopeTarget, setTelescopeTarget] = useState<any | null>(null);

  // MENGAMBIL DATA DARI BACKEND DENGAN ANTI-CACHE
  useEffect(() => {
    const fetchJadwal = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/jadwal", {
          cache: "no-store"
        });
        if (response.ok) {
          const data = await response.json();
          setJadwal(data.reverse());
        }
      } catch (error) {
        console.error("Gagal memuat jadwal", error);
      }
    };
    fetchJadwal();
  }, []);

  return (
    <div className="w-full min-h-screen p-10 flex flex-col items-center justify-center overflow-x-hidden relative bg-transparent">
      
      <div className="w-full max-w-5xl">
        <div className="flex items-center gap-2 mb-8 text-xs font-mono font-bold tracking-widest text-emerald-400 bg-emerald-500/10 w-fit px-4 py-2 rounded-full border border-emerald-500/20">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
          PETUGAS : Luthfi
        </div>
        <div className="bg-[#0a0d16]/10 backdrop-blur-md border border-white/10 rounded-3xl p-8 shadow-[0_0_30px_rgba(168,85,247,0.15)] relative z-10">
          
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 tracking-wide">
                Jadwal Terdaftar
              </h2>
              <p className="text-xs text-gray-500 tracking-widest mt-1">
                Klik pada jadwal untuk membuka visualisasi Lensa Teleskop
              </p>
            </div>
            <Activity className="text-cyan-400/50" size={32} />
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-white/10 text-xs text-gray-400 uppercase tracking-widest">
                  <th className="pb-4 font-bold">Waktu</th>
                  <th className="pb-4 font-bold">Proposal</th>
                  <th className="pb-4 font-bold">Target</th>
                  <th className="pb-4 font-bold">Instrumen</th>
                  <th className="pb-4 font-bold">Status</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                {jadwal.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="py-10 text-center text-gray-500 italic">
                      Jadwal masih kosong. Menunggu inisiasi data...
                    </td>
                  </tr>
                ) : (
                  jadwal.map((item, index) => (
                    <tr 
                      key={index} 
                      onClick={() => setTelescopeTarget(item)} 
                      className="border-b border-white/5 hover:bg-white/10 transition-colors cursor-pointer group"
                    >
                      <td className="py-4 text-emerald-400 font-mono">{item.jam_mulai}:00 - {item.jam_selesai}:00</td>
                      <td className="py-4 text-white font-bold">{item.id_proposal}</td>
                      <td className="py-4 text-purple-400 font-bold group-hover:text-purple-300">{item.target_objek}</td>
                      <td className="py-4 text-gray-300">{item.instrumen}</td>
                      <td className="py-4">
                        <span className="bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider group-hover:bg-cyan-500/40">
                          BIDIK OBJEK
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {telescopeTarget && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#03050a]/90 backdrop-blur-md p-6">
          <div className="bg-[#0a0d16] border border-purple-500/30 rounded-3xl w-full max-w-4xl overflow-hidden shadow-[0_0_80px_rgba(168,85,247,0.15)] animate-in zoom-in-95 duration-300">
            
            <div className="p-6 flex justify-between items-center">
              <div>
                <h2 className="text-2xl font-black text-purple-400 tracking-wide">Tangkapan Lensa Teleskop</h2>
                <p className="text-xs text-gray-400 uppercase tracking-widest mt-1 font-mono">
                  OBJEK: {telescopeTarget.target_objek} | INSTRUMEN: {telescopeTarget.instrumen}
                </p>
              </div>
              <button 
                onClick={() => setTelescopeTarget(null)} 
                className="w-10 h-10 bg-white/5 hover:bg-white/10 border border-white/10 rounded-full flex items-center justify-center text-gray-400 hover:text-white transition-all"
              >
                <X size={20} />
              </button>
            </div>
            
            <div className="relative w-full h-[500px] bg-black rounded-2xl overflow-hidden border-y border-white/5">
              
              <div className="absolute inset-0 pointer-events-none z-10 flex items-center justify-center">
                <div className="w-full h-[1px] bg-emerald-500/40 absolute"></div>
                <div className="h-full w-[1px] bg-emerald-500/40 absolute"></div>
                <div className="w-80 h-80 border border-emerald-500/40 rounded-full absolute"></div>
              </div>
              
              <Canvas camera={{ position: [0, 0, 6] }}>
                <ambientLight intensity={0.05} />
                <directionalLight position={[5, 3, 5]} intensity={2} color="#ffffff" />
                <Stars radius={100} depth={50} count={3000} factor={3} saturation={0} fade speed={1} />
                
                <Suspense fallback={<Loader />}>
                  <RealisticPlanet target={telescopeTarget.target_objek} />
                </Suspense>
                
                <OrbitControls enableZoom={true} autoRotate autoRotateSpeed={0.5} />
              </Canvas>
            </div>
            
            <div className="p-5 text-center bg-[#0a0d16]">
              <p className="text-xs text-gray-500 font-mono tracking-widest">
                Gunakan mouse/touch untuk memutar objek 3D secara bebas.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}