"use client";

import { Calendar, Clock, MapPin, Sun } from "lucide-react";
import { useEffect, useState } from "react";

export default function EnvironmentModule() {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const timeString = now.toLocaleTimeString("en-US", { hour12: false }); // 24-hour format
  const dateString = now
    .toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "2-digit",
    })
    .toUpperCase();
  const dayString = now
    .toLocaleDateString("en-US", { weekday: "long" })
    .toUpperCase();

  return (
    <div className="flex flex-col bg-slate-900 border-2 border-slate-700 rounded-lg overflow-hidden font-mono text-sm shadow-lg w-100 h-full max-w-sm">
      <div className="bg-slate-800 text-slate-300 p-3 border-b border-slate-700 font-bold uppercase tracking-wider flex justify-between items-center">
        <div className="flex items-center gap-2">
          <MapPin className="w-4 h-4 text-cyan-400" />
          <span>OP-AREA STATUS</span>
        </div>
        <div className="flex items-center gap-2 text-green-500 animate-pulse">
          <span className="w-2 h-2 rounded-full bg-green-500"></span>
          <span className="text-xs">LIVE</span>
        </div>
      </div>

      <div className="p-5 flex flex-col gap-6">
        <div className="flex flex-col items-center justify-center bg-slate-950/50 p-4 rounded border border-slate-800">
          <div className="flex items-center gap-2 mb-1 text-slate-500 text-xs font-bold tracking-widest">
            <Clock className="w-3 h-3" />
            <span>LOCAL TIME</span>
          </div>
          <div className="text-4xl font-bold text-white tracking-widest drop-shadow-[0_0_8px_rgba(255,255,255,0.2)]">
            {timeString}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="flex flex-col gap-1 border-l-2 border-cyan-500 pl-3">
            <div className="flex items-center gap-2 text-slate-500 text-xs">
              <Calendar className="w-3 h-3" />
              <span>DATE</span>
            </div>
            <div className="text-slate-200 font-bold">{dateString}</div>
            <div className="text-slate-400 text-xs">{dayString}</div>
          </div>

          <div className="flex flex-col gap-1 border-l-2 border-yellow-500 pl-3">
            <div className="flex items-center gap-2 text-slate-500 text-xs">
              <Sun className="w-3 h-3" />
              <span>WEATHER</span>
            </div>
            <div className="text-slate-200 font-bold uppercase">Clear</div>
            <div className="text-slate-400 text-xs">VIS: OPTIMAL</div>
          </div>
        </div>
      </div>
    </div>
  );
}
