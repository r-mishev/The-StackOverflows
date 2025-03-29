import React, { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet"
import L from "leaflet";
import "leaflet/dist/leaflet.css";

interface CoordinateItem {
  id: string;
  lat: number;
  lng: number;
  timestamp: string;
}

interface MapComponentProps {
  coordinates: CoordinateItem[];
  highlightedId: string | null;
}

const HighlightMarker = ({ item }: { item: CoordinateItem }) => {
  const map = useMap();

  useEffect(() => {
    map.setView([item.lat, item.lng], 14);
  }, [item, map]);

  return (
    <Marker
      position={[item.lat, item.lng]}
      icon={L.icon({
        iconUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png",
        iconSize: [35, 55],
        iconAnchor: [17, 55],
        popupAnchor: [0, -55],
        className: "highlighted-marker",
      })}
    >
      <Popup>
        <strong>ID:</strong> {item.id}
        <br />
        <strong>Time:</strong> {new Date(item.timestamp).toLocaleString()}
      </Popup>
    </Marker>
  );
};

const MapComponent: React.FC<MapComponentProps> = ({ coordinates, highlightedId }) => {
    useEffect(() => {
        import("leaflet").then((L) => {
          L.Icon.Default.mergeOptions({
            iconUrl: "...",
            iconRetinaUrl: "...",
            shadowUrl: "...",
          });
        });
      }, []);
  return (
    <MapContainer
      center={[52.3676, 4.9041]} // Default to Amsterdam
      zoom={13}
      scrollWheelZoom={true}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; <a href='http://osm.org/copyright'>OpenStreetMap</a> contributors"
      />
      {coordinates.map((item) => (
        highlightedId === item.id ? (
          <HighlightMarker key={item.id} item={item} />
        ) : (
          <Marker key={item.id} position={[item.lat, item.lng]}>
            <Popup>
              <strong>ID:</strong> {item.id}
              <br />
              <strong>Time:</strong> {new Date(item.timestamp).toLocaleString()}
            </Popup>
          </Marker>
        )
      ))}
    </MapContainer>
  );
};

export default MapComponent;
