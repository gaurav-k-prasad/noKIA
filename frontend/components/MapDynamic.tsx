import dynamic from "next/dynamic";

// Avoid rendering the entire map at once
const Map = dynamic(() => import("@/components/Map"), {
  ssr: false,
  loading: () => (
    <div className="text-green-500 overflow-hidden rounded-2">
      Initializing Satellite Uplink...
    </div>
  ),
});

export default Map;
