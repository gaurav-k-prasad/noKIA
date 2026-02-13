"use client";
import { useEffect, useState } from "react";
import io from "socket.io-client";

import TeamComms, { CommMessage } from "@/components/Comms";
import EnvironmentModule from "@/components/Environment";
import Map from "@/components/MapDynamic";
import ThreatAlertsModule, { ThreatAlert } from "@/components/ThreatAlert";
// import { mockAlerts, mockNetworkLog } from "@/mock-data/data";

export default function Home() {
  const [units, setUnits] = useState({});

  const [networkLog, setNetworkLog] = useState<CommMessage[]>([]);
  const [alertLog, setAlertLog] = useState<ThreatAlert[]>([]);

  useEffect(() => {
    // Connect to Backend
    const socket = io("http://localhost:8000");

    socket.on("update_state", (data) => {
      setUnits(data);
    });

    socket.on("new_threat", (data) => {
      setAlertLog((prevLog) => [...prevLog, data]);
    });

    socket.on("new_message", (data) => {
      setNetworkLog((prevLog) => [...prevLog, data]);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <main className="relative h-screen w-screen grid grid-cols-4 grid-rows-3 bg-black overflow-hidden gap-6 p-6">
      <div className="row-start-1 row-end-3 col-start-1 col-end-3">
        <Map units={units} />
      </div>

      <div className="row-start-1 row-end-3 col-start-3 col-end-4">
        <TeamComms messages={networkLog} />
      </div>

      <div className="row-start-3 row-end-4 col-start-1 col-end-2">
        <EnvironmentModule />
      </div>

      <div className="row-start-1 row-end-4 col-start-4 col-end-5">
        <ThreatAlertsModule alerts={alertLog} />
      </div>
    </main>
  );
}
