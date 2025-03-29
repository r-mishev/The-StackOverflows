import React, { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { useRouter } from "next/router";

const MapComponent = dynamic(() => import("./MapComponent"), {
  ssr: false,
});

// Dynamically import Map to avoid SSR issue

interface CoordinateItem {
  id: string;
  lat: number;
  lng: number;
  timestamp: string;
}

const DashboardPage = () => {
  const router = useRouter();
  const [items, setItems] = useState<CoordinateItem[]>([]);
  const [highlightedId, setHighlightedId] = useState<string | null>(null);

  // Simulated login check (replace with real auth logic)
//   useEffect(() => {
//     const isAuthenticated = localStorage.getItem("loggedIn") === "true";
//     if (!isAuthenticated) {
//       router.push("/login");
//     }
//   }, [router]);

  // Simulate fetching coordinates from backend
  useEffect(() => {
    const fetchData = async () => {
      // Simulated data - replace with API call
      const data: CoordinateItem[] = [
        { id: "1", lat: 52.3676, lng: 4.9041, timestamp: "2025-03-29T12:00:00Z" },
        { id: "2", lat: 52.3702, lng: 4.8952, timestamp: "2025-03-29T12:05:00Z" },
        { id: "3", lat: 52.3729, lng: 4.9001, timestamp: "2025-03-29T12:10:00Z" },
      ];
      setItems(data);
    };
    fetchData();
  }, []);

  return (
    <div className="min-h-screen flex">
      <div className="w-3/4 h-screen">
        <MapComponent coordinates={items} highlightedId={highlightedId} />
      </div>
      <div className="w-1/4 h-screen overflow-y-auto bg-white p-4">
        <h2 className="text-xl font-bold mb-4">Detected Items</h2>
        <ul className="space-y-2">
          {items.map((item) => (
            <li
              key={item.id}
              onClick={() => setHighlightedId(item.id)}
              className={`cursor-pointer p-2 rounded-lg border ${
                highlightedId === item.id ? "bg-blue-100 border-blue-500" : "bg-gray-100 border-transparent"
              }`}
            >
              <div className="text-sm">ID: {item.id}</div>
              <div className="text-xs text-gray-600">{new Date(item.timestamp).toLocaleString()}</div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default DashboardPage;
