"use client";

import { Activity, AlertCircle, HeartPulse, User } from "lucide-react";
import { useState } from "react";

// The data structure you described: Keys are names, values are arrays of BPMs
export type HeartCheck = Record<string, number[]>;

export default function HeartCheckModule({ data }: { data: HeartCheck }) {
  const soldiers = Object.keys(data);
  const [selectedSoldier, setSelectedSoldier] = useState<string>(soldiers[0]);

  // If no data is provided, show a fallback
  if (!soldiers.length) {
    return (
      <div className="flex items-center justify-center h-full w-full bg-slate-900 border-2 border-slate-700 rounded-lg text-slate-500 font-mono">
        NO BIOMETRIC DATA AVAILABLE
      </div>
    );
  }

  const selectedData = data[selectedSoldier] || [];
  const currentHR =
    selectedData.length > 0 ? selectedData[selectedData.length - 1] : 0;

  // Logic to determine status and colors based on heart rate
  const getStatus = (hr: number) => {
    if (hr === 0)
      return {
        label: "OFFLINE",
        color: "text-slate-500",
        bg: "bg-slate-500",
        border: "border-slate-500",
      };
    if (hr > 130)
      return {
        label: "CRITICAL",
        color: "text-red-500",
        bg: "bg-red-500",
        border: "border-red-500",
      };
    if (hr > 100)
      return {
        label: "ELEVATED",
        color: "text-yellow-400",
        bg: "bg-yellow-400",
        border: "border-yellow-400",
      };
    if (hr < 50)
      return {
        label: "LOW",
        color: "text-red-500",
        bg: "bg-red-500",
        border: "border-red-500",
      };
    return {
      label: "NOMINAL",
      color: "text-cyan-400",
      bg: "bg-cyan-400",
      border: "border-cyan-400",
    };
  };

  const status = getStatus(currentHR);

  // --- SVG SPARKLINE GENERATOR ---
  // Maps the array of heartbeats to an SVG line path
  const generateChartPath = () => {
    if (selectedData.length === 0) return "";

    // We only want to show the last 20 data points so it doesn't get squished
    const recentData = selectedData.slice(-20);
    const maxDataPoints = 20;

    // Fixed Y-axis scale (40 BPM to 180 BPM)
    const minHR = 40;
    const maxHR = 180;

    return recentData
      .map((hr, index) => {
        // Calculate X coordinate (0 to 100%)
        const x = (index / (maxDataPoints - 1)) * 100;
        // Calculate Y coordinate (0 to 100%, inverted because SVG Y goes top-to-bottom)
        const clampedHr = Math.max(minHR, Math.min(maxHR, hr));
        const y = 100 - ((clampedHr - minHR) / (maxHR - minHR)) * 100;

        return `${index === 0 ? "M" : "L"} ${x} ${y}`;
      })
      .join(" ");
  };

  return (
    <div className="flex flex-row h-full w-full bg-slate-900 border-2 border-slate-700 rounded-lg overflow-hidden font-mono text-sm shadow-lg">
      {/* LEFT PANEL: Soldier Selector */}
      <div className="w-1/3 border-r border-slate-700 flex flex-col bg-slate-900/50">
        <div className="bg-slate-800 text-slate-300 p-3 border-b border-slate-700 font-bold uppercase tracking-wider flex items-center gap-2 text-xs">
          <Activity className="w-4 h-4 text-cyan-500" />
          UNIT VITALS
        </div>

        <div className="flex-1 overflow-y-auto [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar-track]:bg-transparent [&::-webkit-scrollbar-thumb]:bg-slate-700">
          {soldiers.map((soldier) => {
            const isSelected = selectedSoldier === soldier;
            const latestHr = data[soldier][data[soldier].length - 1] || 0;
            const soldierStatus = getStatus(latestHr);

            return (
              <button
                key={soldier}
                onClick={() => setSelectedSoldier(soldier)}
                className={`w-full text-left p-3 border-b border-slate-800 transition-colors flex items-center justify-between ${
                  isSelected
                    ? "bg-slate-800 border-l-4 " + soldierStatus.border
                    : "hover:bg-slate-800/50"
                }`}
              >
                <div className="flex items-center gap-2">
                  <User
                    className={`w-4 h-4 ${isSelected ? "text-white" : "text-slate-500"}`}
                  />
                  <span
                    className={`font-bold uppercase ${isSelected ? "text-white" : "text-slate-400"}`}
                  >
                    {soldier}
                  </span>
                </div>
                {/* Small indicator dot on the list */}
                <div
                  className={`w-2 h-2 rounded-full ${soldierStatus.bg} ${latestHr > 130 ? "animate-pulse" : ""}`}
                ></div>
              </button>
            );
          })}
        </div>
      </div>

      {/* RIGHT PANEL: Heart Rate Display */}
      <div className="w-2/3 flex flex-col p-4 relative overflow-hidden">
        {/* Background Grid Pattern (For tactical look) */}
        <div
          className="absolute inset-0 opacity-10 pointer-events-none"
          style={{
            backgroundImage: "radial-gradient(#475569 1px, transparent 1px)",
            backgroundSize: "20px 20px",
          }}
        ></div>

        {/* Selected Soldier Header */}
        <div className="flex justify-between items-start z-10 mb-1">
          <div>
            <div className="text-slate-400 text-xs mb-1">TARGET ID</div>
            <div className="text-xl font-bold text-white uppercase tracking-wider">
              {selectedSoldier}
            </div>
          </div>
          <div
            className={`flex items-center gap-2 border px-3 py-1 rounded-full bg-slate-950/50 ${status.border}`}
          >
            {currentHR > 130 ? (
              <AlertCircle className={`w-4 h-4 ${status.color}`} />
            ) : (
              <HeartPulse className={`w-4 h-4 ${status.color}`} />
            )}
            <span className={`font-bold text-xs ${status.color}`}>
              {status.label}
            </span>
          </div>
        </div>

        {/* Big Number Display */}
        <div className="flex items-baseline gap-2 z-10 mb-4">
          <div
            className={`text-3xl font-bold tracking-tighter ${status.color}`}
          >
            {currentHR || "--"}
          </div>
          <div className="text-slate-500 font-bold">BPM</div>
        </div>

        {/* SVG Sparkline Chart */}
        <div className="flex-1 mt-auto z-10 relative bg-slate-950/50 rounded border border-slate-800 p-2 h-25">
          <div className="absolute top-2 left-2 text-[10px] text-slate-500">
            T-20s HISTORY
          </div>
          <svg
            className="w-full h-full"
            viewBox="0 0 100 100"
            preserveAspectRatio="none"
          >
            {/* Render the line */}
            <path
              d={generateChartPath()}
              fill="none"
              stroke={currentHR > 130 ? "#ef4444" : "#22d3ee"} // Red if critical, Cyan if normal
              strokeWidth="2"
              strokeLinejoin="round"
              strokeLinecap="round"
            />
          </svg>
        </div>
      </div>
    </div>
  );
}
