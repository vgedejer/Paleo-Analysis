import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

/**
 * ============================================================================
 *  FindMap — a small interactive Leaflet map with a single pin.
 * ============================================================================
 *
 *  Renders OpenStreetMap tiles directly (no iframe embed), so we control the
 *  attribution: OSM credit is kept — it's required by the ODbL license — while
 *  the embed's "Report a problem" link is gone. Zoom/pan work; scroll-wheel zoom
 *  is disabled so scrolling the page doesn't get trapped by the map.
 */

// Leaflet's default marker points at image files by relative URL, which a
// bundler can't resolve. Rebuild the icon from Vite-imported asset URLs so the
// pin actually renders. Defined once at module scope — it's stateless.
const pinIcon = L.icon({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

export function FindMap({ lat, lon, label }: { lat: number; lon: number; label: string }) {
  return (
    <div className="mt-4 overflow-hidden border border-paleo-line">
      <MapContainer
        // MapContainer ignores `center`/`zoom` changes after mount. Keying by the
        // coordinates remounts it when a different item is selected, so the map
        // re-centers on the new point instead of staying put.
        key={`${lat},${lon}`}
        center={[lat, lon]}
        zoom={6}
        scrollWheelZoom={true}
        className="h-48 w-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={[lat, lon]} icon={pinIcon}>
          <Popup>{label}</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}
