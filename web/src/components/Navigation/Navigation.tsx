import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

const NavigationBar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    setIsLoggedIn(localStorage.getItem("loggedIn") === "true");
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("loggedIn");
    window.location.href = "/";
  };

  return (
    <nav className="w-full flex justify-between items-center px-8 py-4 bg-black text-white border-b border-white/10">
      <Link href="/">
        <Button variant="link" className="cursor-pointer text-2xl font-bold text-white p-0 m-0  no-underline hover:no-underline">
          DroneRescue
        </Button>
      </Link>
      <div className="flex gap-4 items-center">
        {!isLoggedIn ? (
          <>
            <Link href="/dashboard">
              <Button variant="ghost" className="cursor-pointer text-white hover:underline no-underline hover:no-underline">
                Dashboard
              </Button>
            </Link>
            <Button onClick={handleLogout} variant="outline" className="cursor-pointer text-white border-white">
              Logout
            </Button>
          </>
        ) : (
          <Link href="/login">
            <Button variant="outline" className="cursor-pointer text-white border-white">
              Login
            </Button>
          </Link>
        )}
      </div>
    </nav>
  );
};

export default NavigationBar;