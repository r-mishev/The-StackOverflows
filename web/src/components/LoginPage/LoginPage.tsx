import React, { useState } from "react";
import { Button } from "../ui/button";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const loginData = {
      email,
      password,
    };

    console.log("Prepared data to send:", loginData);
    // You can later send this via fetch/axios:
    // await fetch('/api/login', { method: 'POST', body: JSON.stringify(loginData) })
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white px-4">
      <form
        onSubmit={handleSubmit}
        className="bg-white/10 p-8 rounded-2xl shadow-md w-full max-w-md space-y-6"
      >
        <h2 className="text-2xl font-bold text-center">Login</h2>

        <div>
          <label className="block mb-2">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-4 py-2 rounded-lg bg-white/20 text-white focus:outline-none"
          />
        </div>

        <div>
          <label className="block mb-2">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full px-4 py-2 rounded-lg bg-white/20 text-white focus:outline-none"
          />
        </div>

        <Button type="submit" className="w-full cursor-pointer">
          Log In
        </Button>
      </form>
    </div>
  );
};

export default LoginPage;