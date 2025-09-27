#!/usr/bin/env python3
"""
🎨 Code Live - Stress Test Art Generator
======================================

This script runs stress tests and generates performance art in real-time.
It's designed to create visual chaos that responds to system performance.
"""

import asyncio
import json
import random
import time
from pathlib import Path
from typing import Dict, List

import aiohttp


class StressTestArtGenerator:
    """Generates art from stress test performance"""

    def __init__(self):
        self.base_url = "http://localhost:8000"  # Adjust to your server
        self.performance_history = []
        self.art_frames = []

    async def run_stress_test(self, duration: int = 60, intensity: int = 10):
        """Run stress test and collect performance data"""

        print(f"🎨 Starting {duration}s stress test with intensity {intensity}")
        print("=" * 50)

        start_time = time.time()
        request_count = 0
        error_count = 0

        # Test endpoints
        endpoints = [
            "/render/rust",
            "/render/go",
            "/render/julia",
            "/render/typescript",
            "/render/python",
        ]

        # Performance tracking
        latencies = []
        throughputs = []
        errors = []

        while time.time() - start_time < duration:
            # Generate burst of requests
            burst_size = random.randint(1, intensity)

            tasks = []
            for _ in range(burst_size):
                endpoint = random.choice(endpoints)
                task = self.make_request(endpoint)
                tasks.append(task)

            # Wait for all requests in burst
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            for result in results:
                request_count += 1
                if isinstance(result, Exception):
                    error_count += 1
                    errors.append(1)
                else:
                    latencies.append(result.get("latency", 0))
                    throughputs.append(1)  # Successful request
                    errors.append(0)

            # Generate art frame
            current_time = time.time() - start_time
            art_frame = self.generate_art_frame(
                current_time,
                latencies[-10:] if latencies else [0],  # Last 10 latencies
                sum(throughputs[-10:]) if throughputs else 0,  # Last 10 throughput
                sum(errors[-10:]) if errors else 0,  # Last 10 errors
            )

            self.art_frames.append(art_frame)

            # Small delay between bursts
            await asyncio.sleep(0.1)

        # Final performance summary
        total_requests = request_count
        total_errors = error_count
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        total_throughput = sum(throughputs)

        print("\n📊 Stress Test Results:")
        print(f"   Total requests: {total_requests}")
        print(f"   Total errors: {total_errors}")
        print(f"   Average latency: {avg_latency:.2f}ms")
        print(f"   Total throughput: {total_throughput} req/s")
        print(f"   Error rate: {(total_errors / total_requests) * 100:.2f}%")

        return {
            "total_requests": total_requests,
            "total_errors": total_errors,
            "avg_latency": avg_latency,
            "total_throughput": total_throughput,
            "error_rate": total_errors / total_requests if total_requests > 0 else 0,
            "art_frames": self.art_frames,
        }

    async def make_request(self, endpoint: str) -> Dict:
        """Make a single request and measure performance"""

        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Generate test code
                test_code = self.generate_test_code()

                async with session.post(
                    f"{self.base_url}{endpoint}",
                    json={"code": test_code},
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        latency = (time.time() - start_time) * 1000  # Convert to ms
                        return {
                            "latency": latency,
                            "status": "success",
                            "result": result,
                        }
                    else:
                        return {
                            "latency": (time.time() - start_time) * 1000,
                            "status": "error",
                            "error": f"HTTP {response.status}",
                        }
        except Exception as e:
            return {
                "latency": (time.time() - start_time) * 1000,
                "status": "error",
                "error": str(e),
            }

    def generate_test_code(self) -> str:
        """Generate random test code for stress testing"""

        test_patterns = [
            # Simple list comprehension
            "[x**2 for x in range(100)]",
            # Nested comprehension
            "[[x*y for y in range(10)] for x in range(10)]",
            # Dictionary comprehension
            "{x: x**2 for x in range(50)}",
            # Complex nested structure
            "[{i: [j**2 for j in range(i)] for i in range(10)} for _ in range(5)]",
            # Fibonacci-like recursion
            "[sum(range(i)) for i in range(20)]",
            # Matrix operations
            "[[i*j for j in range(15)] for i in range(15)]",
        ]

        return random.choice(test_patterns)

    def generate_art_frame(
        self, timestamp: float, latencies: List[float], throughput: float, errors: int
    ) -> Dict:
        """Generate a single art frame based on current performance"""

        # Color based on performance
        if errors > 0:
            # Errors = red
            color = (255, 100, 100)
        elif throughput > 5:
            # High throughput = green
            color = (100, 255, 100)
        else:
            # Low throughput = blue
            color = (100, 100, 255)

        # Brightness based on latency
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        brightness = max(0.1, 1.0 - (avg_latency / 1000.0))

        # Apply brightness
        color = tuple(int(c * brightness) for c in color)

        # Generate particle data
        particle_count = min(100, int(throughput * 10))
        particles = []

        for _ in range(particle_count):
            particle = {
                "x": random.uniform(0, 1000),
                "y": random.uniform(0, 1000),
                "vx": random.uniform(-2, 2),
                "vy": random.uniform(-2, 2),
                "color": color,
                "size": max(1, avg_latency / 100),
                "life": 1.0,
            }
            particles.append(particle)

        return {
            "timestamp": timestamp,
            "color": color,
            "particles": particles,
            "performance": {
                "latency": avg_latency,
                "throughput": throughput,
                "errors": errors,
            },
        }

    def save_art_data(self, results: Dict):
        """Save the generated art data"""

        art_data = {
            "experiment_info": {
                "timestamp": time.time(),
                "duration": 60,  # From stress test
                "total_frames": len(self.art_frames),
            },
            "performance_summary": results,
            "art_frames": self.art_frames,
        }

        output_file = Path("stress_test_art_data.json")
        with open(output_file, "w") as f:
            json.dump(art_data, f, indent=2)

        print(f"🎨 Art data saved to {output_file}")

        # Generate HTML visualization
        self.generate_html_visualization(art_data)

    def generate_html_visualization(self, art_data: Dict):
        """Generate HTML visualization of the stress test art"""

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Live - Stress Test Art</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: #000;
            color: #00ff00;
            margin: 0;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .performance-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(0, 255, 0, 0.1);
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }}
        
        .art-canvas {{
            width: 100%;
            height: 600px;
            border: 2px solid #00ff00;
            border-radius: 10px;
            background: #000;
            position: relative;
            overflow: hidden;
        }}
        
        .particle {{
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
        }}
        
        .controls {{
            text-align: center;
            margin: 20px 0;
        }}
        
        button {{
            background: #00ff00;
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }}
        
        button:hover {{
            background: #00cc00;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Code Live - Stress Test Art</h1>
            <p>Real-time performance metrics transformed into visual art</p>
        </div>
        
        <div class="performance-stats">
            <div class="stat-card">
                <h3>Total Requests</h3>
                <p>{art_data["performance_summary"]["total_requests"]}</p>
            </div>
            <div class="stat-card">
                <h3>Total Errors</h3>
                <p>{art_data["performance_summary"]["total_errors"]}</p>
            </div>
            <div class="stat-card">
                <h3>Avg Latency</h3>
                <p>{art_data["performance_summary"]["avg_latency"]:.2f}ms</p>
            </div>
            <div class="stat-card">
                <h3>Error Rate</h3>
                <p>{art_data["performance_summary"]["error_rate"] * 100:.2f}%</p>
            </div>
        </div>
        
        <div class="controls">
            <button onclick="startAnimation()">Start Art Animation</button>
            <button onclick="stopAnimation()">Stop Animation</button>
        </div>
        
        <div class="art-canvas" id="artCanvas"></div>
    </div>
    
    <script>
        const artFrames = {json.dumps(art_data["art_frames"])};
        let currentFrame = 0;
        let animationId = null;
        
        function startAnimation() {{
            if (animationId) return;
            
            function animate() {{
                const canvas = document.getElementById('artCanvas');
                const frame = artFrames[currentFrame];
                
                // Clear canvas
                canvas.innerHTML = '';
                
                // Set background color based on performance
                const color = frame.color;
                canvas.style.backgroundColor = `rgb(${{color[0]}}, ${{color[1]}}, ${{color[2]}}, 0.1)`;
                
                // Draw particles
                frame.particles.forEach(particle => {{
                    const particleEl = document.createElement('div');
                    particleEl.className = 'particle';
                    particleEl.style.left = particle.x + 'px';
                    particleEl.style.top = particle.y + 'px';
                    particleEl.style.width = particle.size + 'px';
                    particleEl.style.height = particle.size + 'px';
                    particleEl.style.backgroundColor = `rgb(${{particle.color[0]}}, ${{particle.color[1]}}, ${{particle.color[2]}})`;
                    canvas.appendChild(particleEl);
                }});
                
                currentFrame = (currentFrame + 1) % artFrames.length;
                animationId = requestAnimationFrame(animate);
            }}
            
            animate();
        }}
        
        function stopAnimation() {{
            if (animationId) {{
                cancelAnimationFrame(animationId);
                animationId = null;
            }}
        }}
        
        // Auto-start animation
        startAnimation();
    </script>
</body>
</html>
"""

        with open("stress_test_art_visualization.html", "w") as f:
            f.write(html_content)

        print("🎨 HTML visualization generated!")


async def main():
    """Main stress test art generator"""
    generator = StressTestArtGenerator()

    print("🎨 Code Live - Stress Test Art Generator")
    print("=" * 50)
    print("This will run a 60-second stress test and generate art!")
    print("Make sure your server is running on localhost:8000")
    print()

    # Run stress test
    results = await generator.run_stress_test(duration=60, intensity=5)

    # Save art data
    generator.save_art_data(results)

    print("\n🎉 Stress Test Art Generation Complete!")
    print("Open 'stress_test_art_visualization.html' to see the results!")


if __name__ == "__main__":
    asyncio.run(main())
