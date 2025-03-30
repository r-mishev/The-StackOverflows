import React from "react";
import { Button } from "@/components/ui/button";
import { ArrowRight, Shield, Signal, AlertTriangle } from "lucide-react";
import Image from "next/image";

const features = [
  {
    icon: <AlertTriangle className="w-6 h-6 text-red-500" />,
    title: "Rapid Response",
    text: "Autonomous drones deploy within minutes, establishing critical communication in emergency situations.",
  },
  {
    icon: <Signal className="w-6 h-6 text-yellow-400" />,
    title: "Extended Coverage",
    text: "Drones provide mobile signal in areas where traditional networks fail — forests, mountains, and disaster zones.",
  },
  {
    icon: <Shield className="w-6 h-6 text-red-500" />,
    title: "Life-Saving Tech",
    text: "Reduces rescue time by up to 70%, significantly increasing survival chances during critical missions.",
  },
];

const LandingPage = () => {
  return (
    <div className="bg-gradient-to-b from-[#0e0b0b] via-[#1b0d0a] to-[#1a0c0b] text-white font-sans">
      {/* Hero Section */}
      <section className="flex flex-col md:flex-row items-center justify-between px-10 md:px-40 py-60">
        <div className="max-w-xl">
          <h1 className="text-4xl md:text-5xl font-bold leading-tight mb-6 text-white">
            When Signals Fail, <br /> We Prevail
          </h1>
          <p className="text-lg text-orange-100 mb-8">
            SkyGuardian’s drone-based emergency signal service bridges the communication gap in remote areas, allowing stranded people to contact emergency services where traditional networks fail.
          </p>
          <div className="flex gap-4">
            <Button className="bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-400 hover:to-red-500 text-white px-6 py-3 text-lg font-semibold rounded">
              <a href="/contactus">Request Service</a>
            </Button>
            <Button variant="outline" className="border-red-400 text-red-400 hover:bg-red-600 hover:text-white px-6 py-3 text-lg font-semibold">
              <a href="#tech">Learn More</a>
            </Button>
          </div>
        </div>
        <div className="mt-12 md:mt-0">
          <Image src="/SkyGuardian-logo-drone.png" alt="SkyGuardian Drone" width={220} height={220} />
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-10 bg-[#1e0e0c] text-center" id="services">
        <h2 className="text-3xl font-bold mb-2 text-white">Lifesaving Features</h2>
        <div className="h-1 w-12 bg-red-500 mx-auto mb-10 rounded"></div>
        <div className="grid md:grid-cols-3 gap-8">
          {features.map((f, i) => (
            <div key={i} className="bg-[#2b1511] rounded-xl p-6 shadow-xl text-left border border-red-900">
              <div className="mb-4">
                <div className="w-12 h-12 rounded-full bg-[#3c1a14] flex items-center justify-center">
                  {f.icon}
                </div>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">{f.title}</h3>
              <p className="text-sm text-orange-100">{f.text}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section id="tech" className="bg-[#140c0c] px-10 py-24">
        <h2 className="text-3xl font-bold text-center mb-2 text-white">How It Works</h2>
        <div className="h-1 w-12 bg-red-500 mx-auto mb-12 rounded"></div>
        <div className="grid md:grid-cols-2 gap-16 items-center mx-10">
          <div>
            <h3 className="text-2xl font-semibold mb-2 text-white">Emergency Detection</h3>
            <p className="text-orange-100">
              Our system patrols areas with poor service and offers the ability to make emergency calls to lost people.
            </p>
          </div>
          <img src="/FlyingDrone.jpg" className="h-[300px] rounded-xl w-auto" alt="Flying drone" />
          <img src="/Jaliek focus turns to killing.jpg" className="h-[300px] rounded-xl w-auto" alt="Coordinated rescue" />
          <div>
            <h3 className="text-2xl font-semibold mb-2 text-white">Coordinated Rescue</h3>
            <p className="text-orange-100">
              With connection restored, emergency teams can coordinate efforts, send instructions, and rescue faster.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="text-center text-sm text-orange-200 py-6 bg-[#1a0c0b] border-t border-red-800">
        © {new Date().getFullYear()} SkyGuardian. All rights reserved.
      </footer>
    </div>
  );
};

export default LandingPage;