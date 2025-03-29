import React from "react";
import { Button } from "../ui/button";

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center px-6">
      <h1 className="text-4xl md:text-6xl font-bold mb-4 text-center">
        Revolutionizing Search & Rescue
      </h1>
      <p className="text-lg md:text-xl mb-8 text-center max-w-2xl">
        Our autonomous drones use cutting-edge AI and thermal imaging to locate missing persons faster and more efficiently than ever before.
      </p>
      <Button className="text-lg px-6 py-3">
        Get Started 
      </Button>

      <div className="mt-16 w-full max-w-4xl grid md:grid-cols-3 gap-8">
        <div className="bg-white/10 rounded-2xl p-6 shadow-lg">
          <h2 className="text-xl font-semibold mb-2">AI-Powered Vision</h2>
          <p>
            Advanced algorithms scan and identify heat signatures and human forms in real time.
          </p>
        </div>
        <div className="bg-white/10 rounded-2xl p-6 shadow-lg">
          <h2 className="text-xl font-semibold mb-2">All-Terrain Ready</h2>
          <p>
            Drones operate in forests, mountains, and urban areas—day or night, rain or shine.
          </p>
        </div>
        <div className="bg-white/10 rounded-2xl p-6 shadow-lg">
          <h2 className="text-xl font-semibold mb-2">Instant Alerts</h2>
          <p>
            Immediate updates and location data sent directly to rescue teams.
          </p>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;