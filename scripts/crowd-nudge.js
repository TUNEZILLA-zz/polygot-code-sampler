#!/usr/bin/env node
/**
 * Crowd Control / Nudge Test WebSocket Server
 * Simulates audience participation for CodeSampler Live
 */

const WebSocket = require("ws");

const PORT = 8765;

console.log("👥 Crowd Control WebSocket Server Starting...");
console.log(`📡 Listening on ws://localhost:${PORT}`);

const wss = new WebSocket.Server({ port: PORT }, () =>
  console.log(`✅ [Crowd] WebSocket listening on ws://localhost:${PORT}`)
);

let kickCount = 0;
let intensity = 1.0;
let hue = 0;

wss.on("connection", (ws) => {
  console.log("🔗 Crowd client connected");
  
  // Demo pings every 5s
  const demoInterval = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      intensity = Math.max(0.1, Math.min(3, intensity + (Math.random() - 0.5) * 0.2));
      hue = (hue + Math.random() * 10) % 360;
      
      const message = {
        type: "nudge",
        deltaIntensity: (Math.random() - 0.5) * 0.1,
        deltaHue: Math.random() * 5,
        timestamp: Date.now()
      };
      
      ws.send(JSON.stringify(message));
      console.log(`📨 Crowd nudge: intensity=${intensity.toFixed(2)}, hue=${hue.toFixed(1)}°`);
    }
  }, 5000);
  
  // Random kicks every 10-15 seconds
  const kickInterval = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      kickCount++;
      const message = {
        type: "kick",
        count: kickCount,
        timestamp: Date.now()
      };
      
      ws.send(JSON.stringify(message));
      console.log(`👟 Crowd kick #${kickCount}!`);
    }
  }, 10000 + Math.random() * 5000);
  
  ws.on("close", () => {
    console.log("🔌 Crowd client disconnected");
    clearInterval(demoInterval);
    clearInterval(kickInterval);
  });
  
  ws.on("error", (err) => {
    console.error("❌ Crowd WebSocket error:", err);
  });
});

wss.on("error", (err) => {
  console.error("❌ Crowd WebSocket Server error:", err);
});

console.log("🎭 Crowd Control ready!");
console.log("📱 Connect your CodeSampler Live to ws://localhost:8765");
console.log("🎛️ Sending demo nudges every 5s and kicks every 10-15s");
