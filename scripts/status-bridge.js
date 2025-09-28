#!/usr/bin/env node
/**
 * Status Bridge - Connects CodeSampler Live to Crowd UI
 * 
 * This bridge connects to your CodeSampler Live app and forwards
 * real-time status (FPS, cap, BPM, governor) to the crowd server.
 * 
 * Usage: node scripts/status-bridge.js
 */

const WebSocket = require("ws");

const CODESAMPLER_WS = "ws://localhost:3000"; // Your CodeSampler Live WebSocket
const CROWD_WS = "ws://localhost:8765";      // Crowd server

console.log("📊 STATUS BRIDGE - LIVE MONITORING");
console.log("===================================");
console.log("🔗 Connecting to CodeSampler Live...");
console.log("📡 Forwarding status to crowd server...");

let codesamplerWs = null;
let crowdWs = null;

// Connect to CodeSampler Live
function connectToCodeSampler() {
  codesamplerWs = new WebSocket(CODESAMPLER_WS);
  
  codesamplerWs.on("open", () => {
    console.log("✅ Connected to CodeSampler Live");
    connectToCrowd();
  });
  
  codesamplerWs.on("message", (data) => {
    try {
      const msg = JSON.parse(data);
      if (msg.type === "status" || msg.fps || msg.cap || msg.bpm) {
        // Forward status to crowd server
        if (crowdWs && crowdWs.readyState === 1) {
          crowdWs.send(JSON.stringify({
            type: "status",
            fps: msg.fps,
            cap: msg.cap,
            bpm: msg.bpm,
            govCap: msg.govCap
          }));
        }
      }
    } catch (err) {
      // Ignore non-JSON messages
    }
  });
  
  codesamplerWs.on("close", () => {
    console.log("🔌 CodeSampler Live disconnected, reconnecting...");
    setTimeout(connectToCodeSampler, 2000);
  });
  
  codesamplerWs.on("error", (err) => {
    console.log("❌ CodeSampler Live error:", err.message);
    setTimeout(connectToCodeSampler, 2000);
  });
}

// Connect to crowd server
function connectToCrowd() {
  crowdWs = new WebSocket(CROWD_WS);
  
  crowdWs.on("open", () => {
    console.log("✅ Connected to crowd server");
    console.log("📊 Status bridge ready - forwarding live data");
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

// Start the bridge
connectToCodeSampler();

// Graceful shutdown
process.on("SIGINT", () => {
  console.log("\n🛑 Shutting down status bridge...");
  if (codesamplerWs) codesamplerWs.close();
  if (crowdWs) crowdWs.close();
  process.exit(0);
});

console.log("🎛️ Status bridge running - press Ctrl+C to stop");
