import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import { Button } from "@/components/ui/button";
import Image from "next/image";

const NavigationBar = () => {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState<boolean | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem("loggedIn");
    setIsLoggedIn(stored === "true");
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("loggedIn");
    localStorage.removeItem("accessToken");
    setIsLoggedIn(false);
    router.push("/");
  };

  return (
    <nav className="w-full flex justify-between items-center px-8 py-4 bg-[#0e0b0b] text-white border-b border-[#ff471a]/40 shadow-sm">
      <Link href="/" className="flex items-center gap-3 cursor-pointer">
        <Image
          src="/SkyGuardian-logo-text.png"
          alt="SkyGuardian Logo"
          width={180}
          height={40}
          className="hidden md:block"
        />
        <Image
          src="/SkyGuardian-logo-drone.png"
          alt="SkyGuardian Logo Icon"
          width={40}
          height={40}
          className="block md:hidden"
        />
      </Link>

      <div className="flex items-center gap-4">
        {isLoggedIn === null ? null : isLoggedIn ? (
          <>
            <Link href="/dashboard">
              <Button className="bg-gradient-to-r from-yellow-500 to-red-500 text-white font-semibold px-5 py-2 rounded hover:from-yellow-400 hover:to-red-400 transition-all cursor-pointer">
                Dashboard
              </Button>
            </Link>
            <Button
              onClick={handleLogout}
              className="bg-transparent border border-red-500 text-red-400 hover:bg-red-500 hover:text-white transition-all font-semibold px-5 py-2 rounded cursor-pointer"
            >
              Logout
            </Button>
          </>
        ) : (
          <Link href="/login">
            <Button className="bg-gradient-to-r from-yellow-500 to-red-500 text-white font-semibold px-5 py-2 rounded hover:from-yellow-400 hover:to-red-400 transition-all cursro-pointer">
              Login
            </Button>
          </Link>
        )}
      </div>
    </nav>
  );
};

export default NavigationBar;
