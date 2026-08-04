"use client";
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import { Canvas, useFrame } from "@react-three/fiber";
import { Stars, OrbitControls } from "@react-three/drei";
import { useRef } from "react";
import * as THREE from "three";

// KOMPONEN KUSTOM: Gelombang Galaksi Digital yang Padat
function DigitalGalaxy() {
  const groupRef = useRef<THREE.Group>(null);

  // Animasi mengambang yang halus
  useFrame((state, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += delta * 0.03;
      groupRef.current.rotation.z += delta * 0.015;
    }
  });

  return (
    <group ref={groupRef} position={[0, 0, -2]}>
      
      {/* Gelombang 1 (Ungu): Dimiringkan 90 derajat agar melintang di tengah layar */}
      <points rotation={[Math.PI / 2, 0, Math.PI / 4]}>
        <torusKnotGeometry args={[5, 2.5, 300, 80]} />
        <pointsMaterial color="#a855f7" size={0.02} transparent opacity={0.6} />
      </points>
      
      {/* Gelombang 2 (Zamrud): Berpotongan menyilang dari arah berlawanan */}
      <points rotation={[-Math.PI / 2.5, Math.PI / 3, 0]}>
        <torusKnotGeometry args={[6, 2, 300, 80]} />
        <pointsMaterial color="#10b981" size={0.015} transparent opacity={0.5} />
      </points>

      {/* Selimut Kosmik (Cyan): Karena radiusnya 12, kameramu berada di DALAM bola partikel ini, memenuhi semua ruang kosong! */}
      <points>
        <sphereGeometry args={[12, 100, 100]} />
        <pointsMaterial color="#06b6d4" size={0.015} transparent opacity={0.2} />
      </points>

    </group>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id">
      <body className="relative text-white bg-[#03050a] w-full min-h-screen overflow-hidden font-sans">
        
        {/* --- KANVAS 3D GALAKSI --- */}
        <div className="absolute inset-0 z-0 pointer-events-auto">
          <Canvas camera={{ position: [0, 0, 8] }} gl={{ alpha: true, antialias: true }}>
            
            {/* Latar Belakang Bintang Statis */}
            <Stars radius={100} depth={50} count={3000} factor={3} saturation={0} fade speed={1} />
            
            {/* Memanggil Komponen Gelombang Digital Kustom */}
            <DigitalGalaxy />

            {/* Kontrol Kamera (opsional: agar user bisa menggeser pandangan) */}
            <OrbitControls enableZoom={false} autoRotate={false} />
          </Canvas>
        </div>

        {/* --- KONTEN WEB (GLASSMORPHISM) --- */}
        <div className="relative z-10 flex w-full h-screen pointer-events-none">
          {/* Sidebar */}
          <div className="pointer-events-auto">
             <Sidebar />
          </div>
          
          {/* Area Halaman Utama */}
          <main className="flex-1 overflow-y-auto pointer-events-auto">
             {children}
          </main>
        </div>

      </body>
    </html>
  );
}