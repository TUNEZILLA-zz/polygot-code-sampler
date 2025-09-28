#!/usr/bin/env node
/**
 * Smoke Tests for CodeSampler Live
 * 
 * Quick health checks before show-time:
 * - Crowd WebSocket auth + message handling
 * - OSC bridge connectivity
 * - App reachability
 * 
 * Usage: node scripts/smoke-tests.js
 */

const WebSocket = require("ws");
const http = require("http");

console.log("🧪 SMOKE TESTS - PRE-SHOW HEALTH CHECKS");
console.log("======================================");

const tests = [];
let passed = 0;
let failed = 0;

function test(name, fn) {
  tests.push({ name, fn });
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

// Test 1: Crowd WebSocket Auth + Messages
test("Crowd WebSocket Auth + Gov + Set", async () => {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket("ws://127.0.0.1:8765");
    let authOk = false;
    let govOk = false;
    let setOk = false;

    const timeout = setTimeout(() => {
      ws.close();
      reject(new Error("Timeout"));
    }, 5000);

    ws.on("open", () => {
      // Test auth
      ws.send(JSON.stringify({ type: "auth", pin: process.env.CROWD_PIN || "9462" }));
    });

    ws.on("message", (data) => {
      try {
        const msg = JSON.parse(data);
        if (msg.type === "auth" && msg.ok) {
          authOk = true;
          // Test gov
          ws.send(JSON.stringify({ type: "gov", cap: 0.6 }));
        }
        if (msg.type === "gov") {
          govOk = true;
          // Test set
          ws.send(JSON.stringify({ type: "set", hue: 180, intensity: 0.7 }));
        }
        if (msg.type === "set") {
          setOk = true;
          clearTimeout(timeout);
          ws.close();
          resolve();
        }
      } catch (err) {
        // Ignore non-JSON messages
      }
    });

    ws.on("error", (err) => {
      clearTimeout(timeout);
      reject(err);
    });
  });
});

// Test 2: App Reachability
test("App HTTP Reachability", async () => {
  return new Promise((resolve, reject) => {
    const req = http.get("http://127.0.0.1:5173/crowd/", (res) => {
      assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
      resolve();
    });
    
    req.on("error", reject);
    req.setTimeout(3000, () => {
      req.destroy();
      reject(new Error("Timeout"));
    });
  });
});

// Test 3: OSC Bridge UDP Port
test("OSC Bridge UDP Port", async () => {
  return new Promise((resolve, reject) => {
    const dgram = require("dgram");
    const client = dgram.createSocket("udp4");
    
    const message = Buffer.from("/fx/hue 0.5");
    const port = process.env.OSC_UDP_PORT || 57120;
    
    client.send(message, port, "127.0.0.1", (err) => {
      client.close();
      if (err) {
        reject(err);
      } else {
        resolve();
      }
    });
  });
});

// Run all tests
async function runTests() {
  console.log(`Running ${tests.length} tests...\n`);

  for (const test of tests) {
    try {
      console.log(`🧪 ${test.name}...`);
      await test.fn();
      console.log(`✅ ${test.name} - PASSED\n`);
      passed++;
    } catch (err) {
      console.log(`❌ ${test.name} - FAILED: ${err.message}\n`);
      failed++;
    }
  }

  console.log("🧪 SMOKE TEST RESULTS");
  console.log("====================");
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`📊 Total: ${tests.length}`);

  if (failed === 0) {
    console.log("\n🎭 All systems ready for show-time!");
    process.exit(0);
  } else {
    console.log("\n🚨 Some tests failed - check your setup!");
    process.exit(1);
  }
}

runTests().catch(console.error);
