"use client";

import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { CircleMarker, ImageOverlay, MapContainer, Popup } from "react-leaflet";

export default function Map({ units }: { units: any }) {
  const imageUrl = "/satellite-image-map.png";

  const imageWidth = 1500;
  const imageHeight = 1500;

  const bounds: L.LatLngBoundsExpression = [
    [0, 0],
    [imageHeight, imageWidth],
  ];

  return (
    <div className="h-full w-full rounded-lg overflow-hidden bg-slate-900 border-2 border-slate-700 ">
      <MapContainer
        crs={L.CRS.Simple}
        bounds={bounds}
        maxBounds={bounds}
        maxBoundsViscosity={0.5}
        style={{ height: "100%", width: "100%", backgroundColor: "#000000" }}
      >
        <ImageOverlay url={imageUrl} bounds={bounds} />

        {Object.values(units).map((unit: any) => {
          const color = unit.type === "enemy" ? "#ff0000" : "#00ffff";

          return (
            <CircleMarker
              key={unit.id}
              // 4. Coordinates are now [y, x] relative to your image pixels!
              center={[unit.lat, unit.lon]}
              pathOptions={{
                color: color,
                fillColor: color,
                fillOpacity: 0.7,
                radius: 5,
              }}
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
    </div>
  );
}
