"use client";
import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import io from "socket.io-client";

// Avoid rendering the entire map at once
const Map = dynamic(() => import("@/components/Map"), {
  ssr: false,
  loading: () => (
    <div className="text-green-500">Initializing Satellite Uplink...</div>
  ),
});

import TeamComms, { CommMessage } from "@/components/Comms";
import EnvironmentModule from "@/components/Enviornment";
import ThreatAlertsModule, { ThreatAlert } from "@/components/ThreatAlert";

const mockAlerts: ThreatAlert[] = [
  {
    id: "t1",
    type: "biometric",
    severity: "critical",
    message: "Critical heart rate drop detected. Vitals unstable.",
    timestamp: "13:42:05",
    source: "Alpha-2 (Sgt. Miller)",
  },
  {
    id: "t2",
    type: "ddos",
    severity: "critical",
    message:
      "Traffic spike detected. 50,000 req/sec attempting to flood Comm Gateway.",
    timestamp: "13:40:12",
    source: "Firewall Node 3",
  },
  {
    id: "t3",
    type: "intrusion",
    severity: "warning",
    message: "Multiple failed SSH login attempts from unrecognized IP.",
    timestamp: "13:35:00",
    source: "Server IP 192.168.1.105",
  },
  {
    id: "t4",
    type: "visual",
    severity: "info",
    message: "Unidentified UAV (Drone) detected in sector 7 airspace.",
    timestamp: "13:30:44",
    source: "YOLO-Cam-North",
  },
  {
    id: "t5",
    type: "jamming",
    severity: "warning",
    message: "High RF interference detected. Possible signal jamming.",
    timestamp: "13:25:10",
    source: "Radio Tower B",
  },
];

const mockNetworkLog: CommMessage[] = [
  {
    id: "1",
    sender: "System",
    text: "Uplink established. Encryption key verified.",
    timestamp: "08:00:00",
    type: "system",
  },
  {
    id: "2",
    sender: "Center",
    text: "All units, this is Center. Radio check, over.",
    timestamp: "08:00:15",
    type: "center",
  },
  {
    id: "3",
    sender: "Viper-1",
    text: "Center, Viper-1. Reading you five by five.",
    timestamp: "08:00:22",
    type: "soldier",
  },
  {
    id: "4",
    sender: "Viper-2",
    text: "Viper-2 check. Moving to rally point beta.",
    timestamp: "08:00:28",
    type: "soldier",
  },
  {
    id: "5",
    sender: "Center",
    text: "Copy Viper actual. Proceed to coordinates and hold.",
    timestamp: "08:00:35",
    type: "center",
  },
];

export default function Home() {
  const [units, setUnits] = useState({});

  useEffect(() => {
    // Connect to Backend
    const socket = io("http://localhost:8000");

    socket.on("update_state", (data) => {
      setUnits(data);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <main className="relative h-screen w-screen bg-black overflow-hidden">
      {/* <div className="h-150 w-150 z-0">
        <Map units={units} />
      </div> */}

      {/* <div className="w-100 h-125">
        <TeamComms messages={mockNetworkLog} />
      </div> */}

      {/* <div className="w-80">
        <EnvironmentModule />
      </div> */}

      {/* <div className="w-[400px] h-[500px]">
        <ThreatAlertsModule alerts={mockAlerts} />
      </div> */}
    </main>
  );
}
