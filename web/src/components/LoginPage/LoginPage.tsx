import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import axios from "axios";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);
      formData.append("grant_type", "password"); // Required for OAuth2PasswordRequestForm

      const response = await axios.post("http://127.0.0.1:8000/login", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        withCredentials: true, // If you're using cookies/session (optional)
      });

      const { access_token } = response.data;
      if (access_token) {
        localStorage.setItem("loggedIn", "true");
        localStorage.setItem("accessToken", access_token);
        window.location.href = "/dashboard";
      } else {
        setError("Invalid login response.");
      }
    } catch (err: any) {
      if (err.response && err.response.status === 401) {
        setError("Incorrect username or password.");
      } else {
        setError("Login failed. Please try again.");
      }
      console.error("Login error:", err);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white px-4">
      <form
        onSubmit={handleSubmit}
        className="bg-white/10 p-8 rounded-2xl shadow-md w-full max-w-md space-y-6"
      >
        <h2 className="text-2xl font-bold text-center">Login</h2>

        <div>
          <label className="block mb-2">Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
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

        {error && <p className="text-red-400 text-sm text-center">{error}</p>}

        <Button type="submit" className="w-full cursor-pointer">
          Log In
        </Button>
      </form>
    </div>
  );
};

export default LoginPage;
