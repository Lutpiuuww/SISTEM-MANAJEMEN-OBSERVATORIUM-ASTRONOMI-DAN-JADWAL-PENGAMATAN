"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, CalendarDays, Telescope, CloudLightning, Settings, Globe } from "lucide-react";

export default function Sidebar() {
  const pathname = usePathname();

  const menuItems = [
    { name: "Dashboard", icon: <LayoutDashboard size={20} />, path: "/" },
    { name: "Manajemen Jadwal", icon: <CalendarDays size={20} />, path: "/jadwal" },
    { name: "Inisiasi Observasi", icon: <Telescope size={20} />, path: "/observasi" },
    { name: "Pusat Meteorologi", icon: <CloudLightning size={20} />, path: "/cuaca" },
    { name: "Visualizer 3D", icon: <Globe size={20} />, path: "/visualizer" }, // Menu baru ditambahkan di sini
  ];

  return (
    <aside className="w-64 h-screen bg-black/10 backdrop-blur-2xl border-r border-white/10 flex flex-col justify-between py-6 relative">
      {/* HEADER SIDEBAR */}
      <div className="h-24 flex items-center gap-4 px-8 border-b border-white/5">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-400 to-purple-500 flex items-center justify-center shadow-[0_0_15px_rgba(16,185,129,0.4)]">
          <Telescope className="text-black" size={24} />
        </div>
        <div>
          <h1 className="text-lg font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-purple-400 tracking-wider">
            OBSERVA
          </h1>
          <p className="text-[10px] text-gray-500 uppercase tracking-widest font-mono">System 
            astronomi
          </p>
        </div>
      </div>

      {/* MENU NAVIGASI */}
      <div className="flex-1 py-8 px-4 space-y-2">
        {menuItems.map((item) => {
          const isActive = pathname === item.path;
          return (
            <Link key={item.path} href={item.path}>
              <div
                className={`flex items-center gap-4 px-4 py-3.5 rounded-xl transition-all duration-300 group cursor-pointer ${
                  isActive
                    ? "bg-emerald-500/10 border border-emerald-500/30 shadow-[0_0_15px_rgba(16,185,129,0.1)]"
                    : "hover:bg-white/5 border border-transparent"
                }`}
              >
                <div className={`${isActive ? "text-emerald-400" : "text-gray-500 group-hover:text-purple-400"} transition-colors`}>
                  {item.icon}
                </div>
                <span className={`text-sm font-medium ${isActive ? "text-emerald-300" : "text-gray-400 group-hover:text-gray-200"}`}>
                  {item.name}
                </span>
                
                {/* Indikator aktif (Garis hijau di kanan) */}
                {isActive && (
                  <div className="ml-auto w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#10b981]"></div>
                )}
              </div>
            </Link>
          );
        })}
      </div>

      {/* FOOTER SIDEBAR */}
      <div className="p-6 border-t border-white/5">
        <div className="flex items-center gap-3 px-4 py-3 bg-black/40 rounded-xl border border-white/5">
          <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center border border-purple-500/30">
            <span className="text-purple-400 font-bold text-xs">ML</span>
          </div>
          <div className="flex flex-col">
            <span className="text-xs font-bold text-gray-200">Luthfi Fadil</span>
            <span className="text-[10px] text-emerald-400 font-mono">Lead Operator</span>
          </div>
        </div>
      </div>
    </aside>
  );
}