import React, { useEffect, useState, useRef } from "react";
import dynamic from "next/dynamic";
import { useRouter } from "next/router";

const MapComponent = dynamic(() => import("./MapComponent"), {
  ssr: false,
});

interface CoordinateItem {
  id: string;
  latitude: number;
  longitude: number;
  timestamp: string;
  wants_help: boolean;
}

const DashboardPage = () => {
  const router = useRouter();
  const [items, setItems] = useState<CoordinateItem[]>([]);
  const [highlightedId, setHighlightedId] = useState<string | null>(null);
  const ws = useRef<WebSocket | null>(null);

  // Fetch initial list from /people with auth token
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const token = localStorage.getItem("accessToken");
        if (!token) {
          router.push("/login");
          return;
        }

        const res = await fetch(`http://${window.location.hostname}:8000/people`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await res.json();
        if (Array.isArray(data)) {
          setItems(data);
        } else {
          console.error("Expected array but got:", data);
        }
      } catch (err) {
        console.error("Failed to fetch /people:", err);
      }
    };

    fetchInitialData();
  }, [router]);

  // Connect to WebSocket for live updates
  useEffect(() => {
    ws.current = new WebSocket(`ws://${window.location.hostname}:8000/ws`);

    ws.current.onopen = () => {
      console.log("WebSocket connected ✅");
    };

    ws.current.onmessage = (event) => {
      const message = JSON.parse(event.data);

      if (message.type === "new_detection") {
        const newPerson: CoordinateItem = message.data;
        setItems((prevItems) => [...prevItems, newPerson]);
      } else if (message.type === "all_people") {
        if (Array.isArray(message.data)) {
          setItems(message.data);
        }
      }
    };

    ws.current.onerror = (error) => {
      console.error("WebSocket error ❌", error);
    };

    ws.current.onclose = () => {
      console.warn("WebSocket disconnected ⚠️");
    };

    return () => {
      ws.current?.close();
    };
  }, []);

  return (
    <div className="min-h-screen flex">
      <div className="w-3/4 h-screen">
      <MapComponent
  coordinates={items}
  highlightedItem={items.find((i) => i.id === highlightedId) || null}
/>

      </div>
      <div className="w-1/4 h-screen overflow-y-auto bg-white p-4">
        <h2 className="text-xl font-bold mb-4">Detected Items</h2>
        <ul className="space-y-2">
          {Array.isArray(items) &&
            items.map((item) => (
              <li
                key={item.id}
                onClick={() => setHighlightedId(item.id)}
                className={`cursor-pointer p-3 rounded-lg border transition-all duration-200 ${
                  highlightedId === item.id
                    ? "bg-blue-100 border-blue-500"
                    : "bg-gray-100 border-transparent"
                } ${item.wants_help ? "border-red-500 bg-red-100 text-red-900 font-semibold" : "text-black"}`}
              >
                <div className="text-sm">
                  <span className="font-medium">Lat:</span> {item.latitude.toFixed(5)}
                </div>
                <div className="text-sm">
                  <span className="font-medium">Lng:</span> {item.longitude.toFixed(5)}
                </div>
                <div className="text-xs text-gray-600 mt-1">
                  {new Date(item.timestamp).toLocaleString()}
                </div>
              </li>
            ))}
        </ul>
      </div>
    </div>
  );
};

export default DashboardPage;
