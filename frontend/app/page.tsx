"use client";
import dynamic from 'next/dynamic';
import { useEffect, useState } from 'react';
import io from 'socket.io-client';

// Avoid rendering th enetire map at once
const Map = dynamic(() => import('@/components/Map'), {
  ssr: false,
  loading: () => <div className="text-green-500">Initializing Satellite Uplink...</div>
});

export default function Home() {
  const [units, setUnits] = useState<any>({});

  useEffect(() => {
    // Connect to Backend
    const socket = io('http://localhost:8000');

    socket.on('update_state', (data) => {
      setUnits(data);
    });

    return () => { socket.disconnect(); };
  }, []);

  return (
    <main className="relative h-screen w-screen bg-black overflow-hidden">

      {/* HUD OVERLAY (Top Bar) */}
      <div className="absolute top-0 left-0 w-full z-50 bg-linear-to-b from-black to-transparent p-4 pointer-events-none">
        <h1 className="text-3xl font-bold text-green-500 tracking-widest border-b border-green-800 pb-2">
          SENTINEL // COMMAND
        </h1>
        <div className="flex gap-4 mt-2">
          <div className="text-cyan-400 text-sm">FRIENDLIES: {Object.values(units).filter((u: any) => u.type !== 'enemy').length}</div>
          <div className="text-red-500 text-sm animate-pulse">THREATS: {Object.values(units).filter((u: any) => u.type === 'enemy').length}</div>
        </div>
      </div>

      {/* THE MAP */}
      <div className="h-full w-full z-0">
        <Map units={units} />
      </div>

      {/* SIDEBAR LOGS (Optional) */}
      <div className="absolute bottom-5 right-5 z-50 w-64 bg-black/80 border border-green-900 p-2 font-mono text-xs text-green-300">
        <p>&gt; System Online</p>
        <p>&gt; Connected to Neural Core</p>
        <p>&gt; Awaiting Inputs...</p>
      </div>

    </main>
  );
}