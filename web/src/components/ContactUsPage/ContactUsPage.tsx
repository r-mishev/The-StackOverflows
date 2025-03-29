import React from "react";
import { Mail, Phone } from "lucide-react";

const ContactPage = () => {
  return (
    <div className="min-h-screen bg-[#1a2135] text-white px-6 py-16 flex flex-col items-center">
      <div className="max-w-2xl w-full text-center">
        <h1 className="text-4xl font-bold mb-4">Contact Us</h1>
        <p className="text-lg text-gray-300 mb-8">
          Need to reach us? Here's how you can get in touch.
        </p>

        <div className="space-y-6 text-lg bg-[#232b45] p-8 rounded-xl border border-[#2d354d] shadow-lg">
          <div className="flex items-center justify-center gap-3">
            <Mail className="text-red-500" />
            <span>support@skyguardian.io</span>
          </div>
          <div className="flex items-center justify-center gap-3">
            <Phone className="text-yellow-400" />
            <span>+1 (800) 555-DRONE</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactPage;