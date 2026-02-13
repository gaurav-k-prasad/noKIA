"use client";

import {
  AlertTriangle,
  Crosshair,
  HeartPulse,
  Radio,
  ShieldAlert,
  WifiOff,
} from "lucide-react";

export interface ThreatAlert {
  id: string;
  type: "ddos" | "intrusion" | "biometric" | "jamming" | "visual";
  severity: "critical" | "warning" | "info";
  message: string;
  timestamp: string;
  source: string;
}

export default function ThreatAlertsModule({
  alerts,
}: {
  alerts: ThreatAlert[];
}) {
  const getAlertIcon = (type: ThreatAlert["type"]) => {
    switch (type) {
      case "ddos":
        return <ShieldAlert className="w-5 h-5" />;
      case "intrusion":
        return <WifiOff className="w-5 h-5" />;
      case "biometric":
        return <HeartPulse className="w-5 h-5" />;
      case "jamming":
        return <Radio className="w-5 h-5" />;
      case "visual":
        return <Crosshair className="w-5 h-5" />;
      default:
        return <AlertTriangle className="w-5 h-5" />;
    }
  };

  const getSeverityStyles = (severity: ThreatAlert["severity"]) => {
    switch (severity) {
      case "critical":
        return {
          bg: "bg-red-950/40 border-red-500/50",
          text: "text-red-400",
          indicator:
            "bg-red-500 animate-pulse shadow-[0_0_8px_rgba(239,68,68,0.8)]",
        };
      case "warning":
        return {
          bg: "bg-yellow-950/40 border-yellow-500/50",
          text: "text-yellow-400",
          indicator: "bg-yellow-500",
        };
      case "info":
        return {
          bg: "bg-cyan-950/40 border-cyan-500/50",
          text: "text-cyan-400",
          indicator: "bg-cyan-500",
        };
    }
  };

  return (
    <div className="flex flex-col h-full w-full bg-slate-900 border-2 border-slate-700 rounded-lg overflow-hidden font-mono text-sm shadow-lg">
      <div className="bg-slate-800 text-slate-300 p-3 border-b border-slate-700 font-bold uppercase tracking-wider flex justify-between items-center">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-red-500" />
          <span>THREAT DETECT</span>
        </div>
        <div className="bg-red-500/20 text-red-500 px-2 py-0.5 rounded text-xs border border-red-500/50">
          {alerts.filter((a) => a.severity === "critical").length} CRITICAL
        </div>
      </div>

      {/* Alerts List Area */}
      <div
        className="flex-1 overflow-y-auto p-3 space-y-3 
        /* Custom Scrollbar */
        [&::-webkit-scrollbar]:w-1.5
        [&::-webkit-scrollbar-track]:bg-transparent
        [&::-webkit-scrollbar-thumb]:bg-slate-700
        [&::-webkit-scrollbar-thumb]:rounded-full"
      >
        {alerts.length === 0 ? (
          <div className="flex items-center justify-center h-full text-slate-500 italic">
            No active threats detected.
          </div>
        ) : (
          alerts.map((alert) => {
            const styles = getSeverityStyles(alert.severity);
            return (
              <div
                key={alert.id}
                className={`flex items-start gap-3 p-3 rounded border ${styles.bg}`}
              >
                {/* Flashing Indicator Dot for Critical */}
                <div className="pt-1.5">
                  <div
                    className={`w-2 h-2 rounded-full ${styles.indicator}`}
                  ></div>
                </div>

                {/* Icon */}
                <div className={`${styles.text} pt-0.5`}>
                  {getAlertIcon(alert.type)}
                </div>

                {/* Alert Content */}
                <div className="flex-1 flex flex-col">
                  <div className="flex justify-between items-start mb-1">
                    <span
                      className={`font-bold uppercase tracking-wider text-xs ${styles.text}`}
                    >
                      {alert.type} ALERT
                    </span>
                    <span className="text-slate-500 text-[10px]">
                      {alert.timestamp}
                    </span>
                  </div>
                  <div className="text-slate-200 text-xs leading-relaxed mb-1">
                    {alert.message}
                  </div>
                  <div className="text-slate-400 text-[10px] uppercase">
                    SRC: {alert.source}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
