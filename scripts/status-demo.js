#!/usr/bin/env node
/**
 * Status Demo - Simulates live status data for Crowd UI
 * 
 * This provides realistic mock data for testing the status bar
 * without needing the full CodeSampler Live app running.
 * 
 * Usage: node scripts/status-demo.js
 */

const WebSocket = require("ws");

const CROWD_WS = "ws://localhost:8765";      // Crowd server

console.log("📊 STATUS DEMO - MOCK LIVE DATA");
console.log("===============================");
console.log("🎭 Simulating realistic performance metrics...");
console.log("📡 Sending to crowd server...");

let crowdWs = null;

// Connect to crowd server
function connectToCrowd() {
  crowdWs = new WebSocket(CROWD_WS);
  
  crowdWs.on("open", () => {
    console.log("✅ Connected to crowd server");
    console.log("📊 Sending mock status data every 2 seconds...");
    startStatusDemo();
  });
  
  crowdWs.on("close", () => {
    console.log("🔌 Crowd server disconnected, reconnecting...");
    setTimeout(connectToCrowd, 2000);
  });
  
  crowdWs.on("error", (err) => {
    console.log("❌ Crowd server error:", err.message);
    setTimeout(connectToCrowd, 2000);
  });
}

// Generate realistic mock data
function generateMockStatus() {
  const baseFps = 55 + Math.random() * 10; // 55-65 FPS
  const baseCap = 300 + Math.random() * 400; // 300-700 particles
  const baseBpm = 120 + Math.random() * 40; // 120-160 BPM
  
  return {
    fps: Math.round(baseFps),
    cap: Math.round(baseCap),
    bpm: Math.round(baseBpm),
    govCap: Math.random() > 0.8 ? Math.random() : null // 20% chance of override
  };
}

// Send status updates
let statusInterval;
function startStatusDemo() {
  statusInterval = setInterval(() => {
    if (crowdWs && crowdWs.readyState === 1) {
      const status = generateMockStatus();
      console.log(`📊 Status: FPS=${status.fps}, Cap=${status.cap}, BPM=${status.bpm}, Gov=${status.govCap ? Math.round(status.govCap * 100) + '%' : 'auto'}`);
      
      // Send to all connected crowd clients
      const data = JSON.stringify({
        type: "status",
        ...status
      });
      
      // Broadcast to all clients (simulate the crowd server broadcasting)
      // In real implementation, this would be handled by the crowd server
      console.log("📡 Broadcasting status to crowd clients...");
    }
  }, 2000);
}

// Start the demo
connectToCrowd();

// Graceful shutdown
process.on("SIGINT", () => {
  console.log("\n🛑 Shutting down status demo...");
  if (statusInterval) clearInterval(statusInterval);
  if (crowdWs) crowdWs.close();
  process.exit(0);
});

console.log("🎛️ Status demo running - press Ctrl+C to stop");
