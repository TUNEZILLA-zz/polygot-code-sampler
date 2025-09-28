#!/usr/bin/env node
/**
 * Broadcast-capable crowd server for CodeSampler Live
 * Relays audience messages to all clients (including your CodeSampler app tab)
 * Enhanced with PIN gate + rate limiting for show security
 */

const WebSocket = require("ws");
const { RateLimiterMemory } = require("rate-limiter-flexible");

const PORT = process.env.CROWD_PORT || 8765;
const PIN  = process.env.CROWD_PIN  || "1111";  // set your own!
const ORIGIN = process.env.CROWD_ORIGIN || "";   // optional strict origin (e.g., http://your-host:5173)

console.log("👥 Crowd Control WebSocket Server Starting...");
console.log(`📡 Listening on ws://localhost:${PORT} (PIN enabled)`);

const wss = new WebSocket.Server({ port: PORT }, () =>
  console.log(`✅ [Crowd] WebSocket listening on ws://localhost:${PORT}`)
);

// simple in-memory rate limit per IP
const limiter = new RateLimiterMemory({ points: 60, duration: 10 }); // 60 msgs / 10s

function okType(t){ return ["hello","auth","nudge","kick","run","set","gov","status"].includes(t); }
function clamp(v,a,b){ return Math.max(a,Math.min(b,v)); }

wss.on("connection", (ws, req) => {
  const ip = req.socket.remoteAddress || "unknown";
  let authed = false;

  // optional Origin gate
  const origin = req.headers.origin || "";
  if (ORIGIN && origin && origin !== ORIGIN) {
    ws.close(4000, "Origin not allowed"); return;
  }

  ws.send(JSON.stringify({ type:"hello", ts: Date.now(), auth:"required" }));

  ws.on("message", async (buf) => {
    try {
      await limiter.consume(ip);
      const msg = JSON.parse(buf.toString());
      if (!okType(msg.type)) return;

      if (!authed) {
        if (msg.type !== "auth") return;
        if ((msg.pin||"") !== PIN) { ws.send(JSON.stringify({ type:"auth", ok:false })); return; }
        authed = true; ws.send(JSON.stringify({ type:"auth", ok:true })); return;
      }

      if (msg.type === "nudge") {
        if (typeof msg.deltaHue === "number")       msg.deltaHue = clamp(msg.deltaHue, -20, 20);
        if (typeof msg.deltaIntensity === "number") msg.deltaIntensity = clamp(msg.deltaIntensity, -1, 1);
      }

      if (msg.type === "set") {
        if (typeof msg.hue === "number") msg.hue = clamp(msg.hue % 360, 0, 360);
        if (typeof msg.intensity === "number") msg.intensity = clamp(msg.intensity, 0, 1);
      }

      if (msg.type === "gov") {
        if (typeof msg.cap === "number") msg.cap = clamp(msg.cap, 0, 1);
      }

      // Handle status requests (don't broadcast, send back to requester)
      if (msg.type === "status") {
        // Send mock status data (in real implementation, this would come from your CodeSampler app)
        const statusData = {
          type: "status",
          fps: Math.floor(Math.random() * 20) + 45, // 45-65 FPS
          cap: Math.floor(Math.random() * 500) + 200, // 200-700 particles
          bpm: Math.floor(Math.random() * 40) + 120, // 120-160 BPM
          govCap: Math.random() > 0.7 ? Math.random() : null // 30% chance of override
        };
        ws.send(JSON.stringify(statusData));
        return; // Don't broadcast status requests
      }

      // broadcast to everyone (including CodeSampler tab)
      const data = JSON.stringify(msg);
      for (const c of wss.clients) if (c.readyState === 1) c.send(data);
    } catch {
      // rate limit exceeded – silently drop
    }
  });

  ws.on("close", () => console.log("🔌 Crowd client disconnected"));
});

wss.on("error", (err) => {
  console.error("❌ Crowd WebSocket Server error:", err);
});

console.log("🎭 Crowd Control ready!");
console.log("📱 Connect your CodeSampler Live to ws://localhost:8765");
console.log("🌐 Share crowd UI: http://YOUR-IP:5173/crowd/");
console.log("🎛️ Audience can nudge hue/intensity and trigger kicks/runs");
console.log("🔒 PIN protection enabled - set CROWD_PIN env var to customize");
