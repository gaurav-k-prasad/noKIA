import random
from datetime import datetime


class Simulator:
    def __init__(self) -> None:
        self.threat_id = 0
        self.msg_id = 0

        self.threat_configs = {
            "biometric": {
                "severity": ["critical", "warning"],
                "sources": [
                    "Alpha-1 (Capt. Price)",
                    "Bravo-6 (Ghost)",
                    "Delta-4 (Sgt. Garrick)",
                ],
                "messages": [
                    "Critical heart rate drop detected. Vitals unstable.",
                    "Elevated stress levels detected. Adrenaline spike.",
                    "Biometric link lost. Signal offline.",
                ],
            },
            "ddos": {
                "severity": ["critical"],
                "sources": ["Firewall Node 3", "External Gateway", "Mainframe Buffer"],
                "messages": [
                    "Traffic spike: {req} req/sec attempting to flood Comm Gateway.",
                    "Inbound UDP flood detected on port 80.",
                    "Syn-flood attack detected from multiple origins.",
                ],
            },
            "intrusion": {
                "severity": ["warning", "critical"],
                "sources": [
                    "Server IP 192.168.1.{ip}",
                    "Internal DB Node",
                    "Auth-Vault-01",
                ],
                "messages": [
                    "Multiple failed SSH login attempts.",
                    "Unauthorized access attempt to secure directory.",
                    "Brute force signature detected on admin panel.",
                ],
            },
            "visual": {
                "severity": ["info", "warning"],
                "sources": ["YOLO-Cam-North", "Thermal-Sentry-02", "Drone-Scan-Alpha"],
                "messages": [
                    "Unidentified UAV detected in sector {sector} airspace.",
                    "Motion detected in restricted zone.",
                    "Thermal signature detected behind Perimeter Wall.",
                ],
            },
            "jamming": {
                "severity": ["warning"],
                "sources": ["Radio Tower B", "SATCOM-Link-04", "Field Comms Hub"],
                "messages": [
                    "High RF interference detected. Possible signal jamming.",
                    "Frequency hopping detected on encrypted channel.",
                    "Signal-to-noise ratio falling below operational threshold.",
                ],
            },
        }

        self.call_signs = ["Viper-1", "Viper-2", "Ghost-Actual", "Saber-6", "Raven-04"]
        self.sol_ids = list(range(5))

        self.dialogue_pools = {
            "system": [
                "Uplink established. Encryption key verified.",
                "Satellite handshake complete. Low latency mode active.",
                "Packet loss detected on Sub-net 4. Re-routing...",
                "Secure burst transmission received.",
                "Heads-up display (HUD) sync successful.",
            ],
            "center": [
                "All units, this is Center. Radio check, over.",
                "Copy {unit}. Proceed to rally point {point}.",
                "Visual confirmed on your position. Support is 5 mikes out.",
                "Hold position. High-value target moving into sector {sector}.",
                "RTB (Return to Base) authorized. Good work today.",
            ],
            "soldier": [
                "Center, {unit}. Reading you five by five.",
                "Moving to rally point {point}. No contact yet.",
                "Contact! Multiple hostiles at bearing {bearing}.",
                "Requesting extraction at primary LZ. Under heavy fire.",
                "Objective secure. Waiting for further orders.",
            ],
        }

    def next_heart_data(self):
        drift = random.randint(60, 120)

        sol = random.choice(self.sol_ids)
        return {"id": sol, "name": self.call_signs[sol], "value": drift}

    def next_threat(self):
        self.threat_id += 1

        t_type = random.choice(list(self.threat_configs.keys()))
        config = self.threat_configs[t_type]

        msg = random.choice(config["messages"]).format(
            req=random.randint(10000, 99000),
            sector=random.randint(1, 12),
            ip=random.randint(100, 255),
        )

        source = random.choice(config["sources"]).format(ip=random.randint(100, 255))

        return {
            "id": f"t{self.threat_id}",
            "type": t_type,
            "severity": random.choice(config["severity"]),
            "message": msg,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "source": source,
        }

    def next_message(self, force_type=None):
        self.msg_id += 1

        # Determine message type (weighted slightly toward soldiers/center)
        t_type = (
            force_type
            or random.choices(["system", "center", "soldier"], weights=[15, 35, 50])[0]
        )

        # Contextual variables
        unit = random.choice(self.call_signs)
        point = random.choice(["Alpha", "Beta", "Gamma", "ZULU"])
        sector = random.randint(1, 24)
        bearing = random.randint(0, 359)

        # Pick and format text
        text_template = random.choice(self.dialogue_pools[t_type])
        text = text_template.format(
            unit=unit, point=point, sector=sector, bearing=bearing
        )

        # Assign sender based on type
        sender = (
            "System"
            if t_type == "system"
            else ("Center" if t_type == "center" else unit)
        )

        return {
            "id": str(self.msg_id),
            "sender": sender,
            "text": text,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "type": t_type,
        }
