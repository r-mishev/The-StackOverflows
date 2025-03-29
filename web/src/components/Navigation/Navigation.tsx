import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import { Button } from "@/components/ui/button";

const NavigationBar = () => {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState<boolean | null>(null); // null = unknown

  useEffect(() => {
    const stored = localStorage.getItem("loggedIn");
    setIsLoggedIn(stored === "true");
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("loggedIn");
    router.push("/");
  };

  return (
    <nav className="w-full flex justify-between items-center px-6 py-4 bg-black text-yellow-300 border-b border-yellow-400">
      <Link href="/" className="block">
        <img
          src="/SkyGuardian-logo-text.png"
          alt="SkyGuardian Logo Text"
          className="hidden md:block h-12"
        />
        <img
          src="/SkyGuardian-logo-drone.png"
          alt="SkyGuardian Logo Drone"
          className="block md:hidden h-10"
        />
      </Link>

      <div className="flex items-center gap-4">
        {isLoggedIn === null ? null : isLoggedIn ? (
          <>
            <Link href="/dashboard">
              <Button className="cursor-pointer border border-yellow-300 bg-black text-yellow-300 hover:bg-yellow-400 hover:text-black">
                Dashboard
              </Button>
            </Link>
            <Button
              className="cursor-pointer border border-yellow-300 bg-black text-yellow-300 hover:bg-yellow-400 hover:text-black"
              onClick={handleLogout}
            >
              Logout
            </Button>
          </>
        ) : (
          <Link href="/login">
            <Button className="cursor-pointer border border-yellow-300 bg-black text-yellow-300 hover:bg-yellow-400 hover:text-black">
              Login
            </Button>
          </Link>
        )}
      </div>
    </nav>
  );
};

export default NavigationBar;
