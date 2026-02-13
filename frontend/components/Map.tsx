"use client";

import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { CircleMarker, ImageOverlay, MapContainer, Popup } from "react-leaflet";

export default function Map({ units }: { units: any }) {
  const imageUrl = "/satellite-image-map.png";

  const imageWidth = 512;
  const imageHeight = 512;

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
        {/* {JSON.stringify(units)} */}
        {Object.values(units).map((unit: any, i) => {
          const d = unit.data;
          const alpha = unit.status == "active" ? "f" : "8";
          return (
            <>
              <CircleMarker
                key={i}
                center={[d.pos[0], d.pos[1]]}
                pathOptions={{
                  color: "#0ff" + alpha,
                  fillColor: "#0ff" + alpha,
                  fillOpacity: 0.7,
                  radius: 5,
                }}
              >
                <Popup>
                  <div className="text-black font-bold">
                    ID: {d.id} <br />
                  </div>
                </Popup>
              </CircleMarker>
              {d.calculated_threats.map((enemy, k) => {
                return (
                  <CircleMarker
                    key={k}
                    center={[enemy.pos_x, enemy.pos_y]}
                    pathOptions={{
                      color: "#f00" + alpha,
                      fillColor: "#f00" + alpha,
                      fillOpacity: 0.7,
                      radius: 5,
                    }}
                  >
                    <Popup>
                      <div className="text-black font-bold">
                        By Soldier: {d.id} <br />
                      </div>
                    </Popup>
                  </CircleMarker>
                );
              })}
            </>
          );
        })}
      </MapContainer>
    </div>
  );
}
