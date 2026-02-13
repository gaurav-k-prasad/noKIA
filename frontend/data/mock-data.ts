import { CommMessage } from "@/components/Comms";
import { HeartCheck } from "@/components/HeartCheck";
import { ThreatAlert } from "@/components/ThreatAlert";

export const mockAlerts: ThreatAlert[] = [
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

export const mockNetworkLog: CommMessage[] = [
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

// Mock data: Keys are names, values are arrays of historical BPM data
export const mockHeartData: HeartCheck = {
  "Rahul Kumar": [
    72, 74, 75, 76, 75, 78, 80, 81, 79, 82, 85, 84, 86, 88, 87, 89, 92, 95, 96,
    98,
  ], // Normal/Elevated
  "Gaurav Prasad": [
    110, 115, 120, 125, 130, 135, 140, 142, 145, 148, 150, 155, 160, 158, 162,
    165, 168, 170, 172, 175,
  ], // Critical Spike
  "Ananya Jain": [
    65, 66, 65, 64, 66, 67, 68, 65, 64, 65, 66, 67, 65, 64, 66, 65, 64, 63, 65,
    66,
  ], // Stable resting
  "Vasquez Hatim": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // Offline / Sensor loss
};