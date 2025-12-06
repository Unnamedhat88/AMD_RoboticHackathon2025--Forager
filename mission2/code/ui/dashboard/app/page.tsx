"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const fetchStatus = async () => {
    try {
      const res = await fetch("http://localhost:8000/status");
      if (res.ok) {
        const data = await res.json();
        setStatus(data);
      }
    } catch (error) {
      console.error("Failed to fetch status:", error);
    } finally {
      setLoading(false);
    }
  };

  const sendCommand = async (cmd: "start" | "stop") => {
    try {
      await fetch(`http://localhost:8000/${cmd}`, { method: "POST" });
      fetchStatus();
    } catch (error) {
      console.error(`Failed to send ${cmd}:`, error);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <main className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-gray-800">Grocery Robot Dashboard</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Status Card */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4 text-gray-700">System Status</h2>
            {loading ? (
              <p>Loading...</p>
            ) : status ? (
              <div className="space-y-2">
                <p><span className="font-medium">State:</span> {status.state}</p>
                <p><span className="font-medium">Running:</span> {status.running ? "Yes" : "No"}</p>
                <p><span className="font-medium">Current Item:</span> {status.current_item || "None"}</p>
              </div>
            ) : (
              <p className="text-red-500">Offline</p>
            )}

            <div className="mt-6 flex space-x-4">
              <button
                onClick={() => sendCommand("start")}
                className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition"
              >
                Start Robot
              </button>
              <button
                onClick={() => sendCommand("stop")}
                className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
              >
                Stop Robot
              </button>
            </div>
          </div>

          {/* Navigation Card */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4 text-gray-700">Navigation</h2>
            <a
              href="/inventory"
              className="block w-full text-center px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
            >
              View Inventory
            </a>
          </div>
        </div>
      </main>
    </div>
  );
}
