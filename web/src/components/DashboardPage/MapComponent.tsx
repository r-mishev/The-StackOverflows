import React, { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

interface CoordinateItem {
  id: string;
  latitude: number;
  longitude: number;
  timestamp: string;
  wants_help: boolean;
}

interface MapComponentProps {
    coordinates: CoordinateItem[];
    highlightedItem: CoordinateItem | null;
  }

const defaultIcon = L.icon({
    iconUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png",
    iconRetinaUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon-2x.png",
    shadowUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
  });
  
  const highlightIcon = L.icon({
    iconUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png",
    iconRetinaUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon-2x.png",
    shadowUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png",
    iconSize: [35, 55],
    iconAnchor: [17, 55],
    popupAnchor: [0, -55],
    shadowSize: [41, 41],
  });
  
  const redIcon = L.icon({
    iconUrl: '/marker.svg',
    shadowUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
  });
  
const HighlightMarker = ({ item }: { item: CoordinateItem }) => {
  const map = useMap();

  useEffect(() => {
    map.flyTo([item.latitude, item.longitude], 15, {
      animate: true,
      duration: 1.5,
    });
  }, [item, map]);

  return (
    <Marker
      position={[item.latitude, item.longitude]}
      icon={item.wants_help ? redIcon : highlightIcon}
    >
      <Popup>
        <strong>Lat:</strong> {item.latitude.toFixed(5)}
        <br />
        <strong>Lng:</strong> {item.longitude.toFixed(5)}
        <br />
        <strong>Time:</strong> {new Date(item.timestamp).toLocaleString()}
      </Popup>
    </Marker>
  );
};

const MapComponent: React.FC<MapComponentProps> = ({ coordinates, highlightedItem }) => {
  useEffect(() => {
    import("leaflet").then((L) => {
      L.Icon.Default.mergeOptions({
        iconUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png",
        iconRetinaUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon-2x.png",
        shadowUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png",
      });
    });
  }, []);

  return (
    <MapContainer
      center={[52.3676, 4.9041]}
      zoom={13}
      scrollWheelZoom={true}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; <a href='http://osm.org/copyright'>OpenStreetMap</a> contributors"
      />

{coordinates.map((item) =>
  highlightedItem?.id === item.id ? (
    <HighlightMarker key={item.id} item={item} />
  ) : (
    <Marker
      key={item.id}
      position={[item.latitude, item.longitude]}
      icon={item.wants_help ? redIcon : defaultIcon}
    >
      <Popup>
        <strong>Lat:</strong> {item.latitude.toFixed(5)}
        <br />
        <strong>Lng:</strong> {item.longitude.toFixed(5)}
        <br />
        <strong>Time:</strong> {new Date(item.timestamp).toLocaleString()}
      </Popup>
    </Marker>
  )
)}

    </MapContainer>
  );
};

export default MapComponent;
