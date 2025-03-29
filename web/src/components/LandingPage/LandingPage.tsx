import React from "react";
import { Button } from "@/components/ui/button";
import { ArrowRight, Shield, Signal, AlertTriangle } from "lucide-react";
import Image from "next/image";

const features = [
  {
    icon: <AlertTriangle className="w-6 h-6 text-red-400" />,
    title: "Rapid Response",
    text: "Autonomous drones deploy within minutes, establishing critical communication in emergency situations.",
  },
  {
    icon: <Signal className="w-6 h-6 text-yellow-400" />,
    title: "Extended Coverage",
    text: "Drones provide mobile signal in areas where traditional networks fail — forests, mountains, and disaster zones.",
  },
  {
    icon: <Shield className="w-6 h-6 text-red-400" />,
    title: "Life-Saving Tech",
    text: "Reduces rescue time by up to 70%, significantly increasing survival chances during critical missions.",
  },
];

const LandingPage = () => {
  return (
    <div className="bg-[#121A2F] text-white font-sans ">
      {/* Hero Section */}
      <section className="flex flex-col md:flex-row items-center justify-between px-40 py-50 bg-gradient-to-r from-[#141D3A] to-[#1F2C4C]">
        <div className="max-w-xl">
          <h1 className="text-4xl md:text-5xl font-bold leading-tight mb-6">
            When Signals Fail, <br /> We Prevail
          </h1>
          <p className="text-lg text-gray-300 mb-8">
            SkyGuardian’s drone-based emergency signal service bridges the communication gap in remote areas, allowing stranded people to contact emergency services where traditional networks fail.
          </p>
          <div className="flex gap-4">
            <Button className="bg-red-500 hover:bg-red-400 text-white px-6 py-3 text-lg font-semibold rounded">
                <a href="/contactus">
              Request Service
              </a>
            </Button>
            <Button variant="outline" className="border-white text-white hover:bg-white hover:text-black px-6 py-3 text-lg font-semibold">
              <a href="#tech">
              Learn More
              </a>
            </Button>
          </div>
        </div>
        <div className="mt-12 md:mt-0">
          <Image src="/SkyGuardian-logo-drone.png" alt="SkyGuardian Drone" width={220} height={220} />
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-10 bg-[#1B2545] text-center" id="services">
        <h2 className="text-3xl font-bold mb-2">Lifesaving Features</h2>
        <div className="h-1 w-12 bg-red-500 mx-auto mb-10 rounded"></div>
        <div className="grid md:grid-cols-3 gap-8">
          {features.map((f, i) => (
            <div key={i} className="bg-[#202B4F] rounded-xl p-6 shadow-lg text-left">
              <div className="mb-4">
                <div className="w-12 h-12 rounded-full bg-[#2B365C] flex items-center justify-center">
                  {f.icon}
                </div>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">{f.title}</h3>
              <p className="text-sm text-gray-300">{f.text}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section  className="bg-[#131C35] px-10 py-24" id="tech">
        <h2 className="text-3xl font-bold text-center mb-2">How It Works</h2>
        <div className="h-1 w-12 bg-red-500 mx-auto mb-12 rounded"></div>
        <div className="grid md:grid-cols-2 gap-16 items-center mx-10">
          <div>
            <h3 className="text-2xl font-semibold mb-2">Emergency Detection</h3>
            <p className="text-gray-300">
              Our system patrol areas with poor service and offer the ability to make an emergency call to lost people.
            </p>
          </div>
          <img src='/flying drone.jpg' className="h-[300px] rounded-xl w-auto"></img>
          <img src='/Jaliek focus turns to killing.jpg' className="h-[300px] rounded-xl w-auto"></img>
          <div>
            <h3 className="text-2xl font-semibold mb-2">Coordinated Rescue</h3>
            <p className="text-gray-300">
              With connection restored, emergency teams can coordinate efforts, send instructions, and rescue faster.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="text-center text-sm text-gray-400 py-6 bg-[#1A2340] border-t border-gray-700">
        © {new Date().getFullYear()} SkyGuardian. All rights reserved.
      </footer>
    </div>
  );
};

export default LandingPage;
