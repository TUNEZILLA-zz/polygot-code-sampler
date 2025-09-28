#!/usr/bin/env node
/**
 * QR Code Generator for Crowd UI Sharing
 * Generates QR code for audience to scan and join
 */

const { execSync } = require('child_process');

// Get local IP address
function getLocalIP() {
  try {
    // Try en0 first (WiFi), then en1 (Ethernet)
    const en0 = execSync('ipconfig getifaddr en0', { encoding: 'utf8' }).trim();
    if (en0 && en0 !== '') return en0;
    const en1 = execSync('ipconfig getifaddr en1', { encoding: 'utf8' }).trim();
    if (en1 && en1 !== '') return en1;
  } catch (e) {
    // Fallback to localhost
  }
  return 'localhost';
}

const MYIP = getLocalIP();
const PORT = process.env.DEV_PORT || '5173';
const CROWD_URL = `http://${MYIP}:${PORT}/crowd/?server=ws://${MYIP}:8765`;

console.log("🎭 CROWD UI QR CODE GENERATOR");
console.log("=============================");
console.log(`📱 Audience URL: ${CROWD_URL}`);
console.log("");

// Try to generate QR code if qrcode-terminal is available
try {
  const qrcode = require('qrcode-terminal');
  qrcode.generate(CROWD_URL, { small: true });
} catch (e) {
  console.log("📋 QR Code not available - install with: npm install -g qrcode-terminal");
  console.log("📋 Or share this URL manually:");
  console.log(`   ${CROWD_URL}`);
}

console.log("");
console.log("🔒 For secure shows, use: make crowd-secure");
console.log("📱 PIN: 9462 (audience will need to enter this)");
console.log("🎛️ Audience can nudge hue/intensity and trigger kicks/runs");
