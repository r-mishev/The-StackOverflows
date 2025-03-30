import React from "react";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-black text-yellow-100 flex flex-col">
      {/* Hero Section */}
      <main className="flex-grow flex flex-col items-center justify-center px-6 py-12">
        <h1 className="text-4xl md:text-6xl font-bold mb-4 text-yellow-300 text-center">
          Revolutionizing Search &amp; Rescue
        </h1>
        <p className="text-lg md:text-xl text-yellow-200 mb-8 text-center max-w-2xl">
          Our autonomous drones use cutting-edge AI and thermal imaging 
          to locate missing persons faster and more efficiently than ever before.
        </p>
        <Button className="bg-yellow-400 text-black hover:bg-yellow-300 px-6 py-3 text-lg">
          Get Started 
          <ArrowRight className="ml-2 w-5 h-5" />
        </Button>
      </main>

      {/* Features Section */}
      <section className="w-full max-w-6xl mx-auto px-6 grid md:grid-cols-3 gap-8 mb-16">
        <div className="bg-white/5 border border-yellow-400 rounded-2xl p-6 shadow-lg">
          <h2 className="text-xl font-semibold mb-2 text-yellow-300">
            AI-Powered Vision
          </h2>
          <p className="text-sm text-yellow-100">
            Advanced algorithms scan and identify heat signatures 
            and human forms in real time.
          </p>
        </div>
        <div className="bg-white/5 border border-yellow-400 rounded-2xl p-6 shadow-lg">
          <h2 className="text-xl font-semibold mb-2 text-yellow-300">
            All-Terrain Ready
          </h2>
          <p className="text-sm text-yellow-100">
            Drones operate in forests, mountains, and urban areas — 
            day or night, rain or shine.
          </p>
        </div>
        <div className="bg-white/5 border border-yellow-400 rounded-2xl p-6 shadow-lg">
          <h2 className="text-xl font-semibold mb-2 text-yellow-300">
            Instant Alerts
          </h2>
          <p className="text-sm text-yellow-100">
            Immediate updates and location data sent directly to rescue teams.
          </p>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
