/**
 * PM2 Ecosystem Configuration for CodeSampler Live
 * 
 * Production process management for:
 * - OSC Bridge (UDP → WebSocket)
 * - Crowd Server (WebSocket with PIN + rate limiting)
 * - Main App (Vite dev server or production build)
 */

module.exports = {
  apps: [
    {
      name: "osc-bridge",
      script: "scripts/osc-bridge.js",
      env: { 
        OSC_UDP_PORT: process.env.OSC_UDP_PORT || 57120, 
        OSC_WS_PORT: process.env.OSC_WS_PORT || 57121 
      },
      restart_delay: 1000,
      max_restarts: 10,
      min_uptime: "10s"
    },
    {
      name: "crowd-server",
      script: "scripts/crowd-server.js",
      env: { 
        CROWD_PORT: process.env.CROWD_PORT || 8765, 
        CROWD_PIN: process.env.CROWD_PIN || "9462", 
        CROWD_ORIGIN: process.env.CROWD_ORIGIN || "" 
      },
      restart_delay: 1000,
      max_restarts: 10,
      min_uptime: "10s"
    },
    {
      name: "app",
      script: "npm",
      args: "run dev",           // or "run preview" / "run start" for prod build
      env: { 
        PORT: process.env.APP_PORT || 5173,
        NODE_ENV: process.env.NODE_ENV || "production"
      },
      restart_delay: 2000,
      max_restarts: 5,
      min_uptime: "30s"
    }
  ]
};
