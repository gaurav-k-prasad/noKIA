"use client";

import L from "leaflet";
import 'leaflet/dist/leaflet.css';
import { CircleMarker, ImageOverlay, MapContainer, Popup } from 'react-leaflet';

export default function Map({ units }: { units: any }) {
  const imageUrl = '/satellite-image-map.png';

  const imageWidth = 800; 
  const imageHeight = 800;

  // 3. Set the bounds: [[bottom, left], [top, right]]
  // In CRS.Simple, it's generally [y, x]. 
  const bounds: L.LatLngBoundsExpression = [
    [0, 0],
    [imageHeight, imageWidth]
  ];

  return (
    <MapContainer
  crs={L.CRS.Simple}
  bounds={bounds}
  maxBounds={bounds} // 👈 This traps the user inside the image!
  maxBoundsViscosity={1.0} // 👈 Makes the edge feel like a solid wall (no bouncing)
  style={{ height: "100%", width: "100%", backgroundColor: "#000000" }}
>
      <ImageOverlay
        url={imageUrl}
        bounds={bounds}
      />

      {Object.values(units).map((unit: any) => {
        const color = unit.type === 'enemy' ? '#ff0000' : '#00ffff';

        return (
          <CircleMarker
            key={unit.id}
            // 4. Coordinates are now [y, x] relative to your image pixels!
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