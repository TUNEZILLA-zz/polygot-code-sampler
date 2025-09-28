#!/usr/bin/env node
/**
 * OSC → WebSocket Bridge for CodeSampler Live
 * Sends OSC from DAW/phone (TouchOSC, Lemur) to browser via WebSocket
 */

const osc = require("osc");
const WebSocket = require("ws");

const WS_PORT = 57121;      // browser connects to ws://localhost:57121
const UDP_PORT = 57120;     // send your OSC here (e.g., /fx/hue 0.42)
const UDP_HOST = "0.0.0.0";

console.log("🎛️ OSC → WebSocket Bridge Starting...");
console.log(`📡 WebSocket: ws://localhost:${WS_PORT}`);
console.log(`📡 OSC UDP: ${UDP_HOST}:${UDP_PORT}`);

const wss = new WebSocket.Server({ port: WS_PORT }, () =>
  console.log(`✅ [OSC→WS] WebSocket listening on ${WS_PORT}`)
);

const udp = new osc.UDPPort({ localAddress: UDP_HOST, localPort: UDP_PORT });
udp.on("ready", () => console.log(`✅ [OSC→WS] UDP listening on ${UDP_HOST}:${UDP_PORT}`));

udp.on("message", (msg) => {
  // msg = { address: "/fx/hue", args:[0.42] }
  console.log(`📨 OSC: ${msg.address} ${msg.args.join(' ')}`);
  
  const payload = JSON.stringify({ 
    address: msg.address, 
    args: msg.args,
    timestamp: Date.now()
  });
  
  wss.clients.forEach((c) => {
    if (c.readyState === 1) {
      c.send(payload);
    }
  });
});

udp.on("error", (err) => {
  console.error("❌ OSC Error:", err);
});

wss.on("connection", (ws) => {
  console.log("🔗 Browser connected to OSC bridge");
  
  ws.on("close", () => {
    console.log("🔌 Browser disconnected from OSC bridge");
  });
  
  ws.on("error", (err) => {
    console.error("❌ WebSocket Error:", err);
  });
});

wss.on("error", (err) => {
  console.error("❌ WebSocket Server Error:", err);
});

udp.open();

console.log("🎭 Ready for OSC control!");
console.log("📱 Send OSC to 127.0.0.1:57120");
console.log("🎛️ Examples:");
console.log("  /fx/hue 0.25");
console.log("  /fx/intensity 0.8");
console.log("  /run");
console.log("  /gov/cap 0.5");
console.log("  /crowd/kick");
