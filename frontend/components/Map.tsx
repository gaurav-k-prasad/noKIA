// frontend/components/Map.tsx
"use client";

import { LatLngTuple } from "leaflet";
import 'leaflet/dist/leaflet.css';
import { CircleMarker, MapContainer, Popup, TileLayer } from 'react-leaflet';

export default function Map({ units }: { units: any }) {
  // Center of map - Siachin Glacier
  const defaultCenter: LatLngTuple = [34.0161, 75.3150];

  return (
    <MapContainer
      center={defaultCenter}
      zoom={15}
      style={{ height: "100%", width: "100%", zIndex: 0 }}
      className="z-0"
    >
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
      />


      {/* Render Units */}
      {Object.values(units).map((unit: any) => {
        // Color Logic: Enemy = Red, Friendly = Cyan
        const color = unit.type === 'enemy' ? '#ff0000' : '#00ffff';

        return (
          <CircleMarker
            key={unit.id}
            center={[unit.lat, unit.lon]}
            pathOptions={{ color: color, fillColor: color, fillOpacity: 0.7, radius: 5 }}
          >
            <Popup>
              <div className="text-black font-bold">
                ID: {unit.id} <br />
                HR: {unit.heart_rate} <br />
                STATUS: {unit.status}
              </div>
            </Popup>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
}