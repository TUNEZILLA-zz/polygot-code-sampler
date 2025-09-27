#!/usr/bin/env python3
"""
🎨 Code Live - Creative Performance Art Experiment
================================================

This experiment turns backend performance metrics into visual art:
- Maps backend performance to color frequencies (like sound → color)
- Creates particle systems that respond to system health
- Generates fractal patterns based on computation depth
- Syncs visual effects to performance beats

Creative Lens: Backend bottlenecks show up as muddy colors or dim sections.
"""

import asyncio
import json
import random
import time
from pathlib import Path
from typing import Dict, List, Tuple


class PerformanceArtGenerator:
    """Generates visual art from performance metrics"""

    def __init__(self):
        self.color_map = {
            "rust": (255, 100, 100),  # Low red
            "go": (100, 255, 100),  # Green
            "julia": (200, 100, 255),  # High violet
            "typescript": (100, 200, 255),  # Blue
            "python": (255, 200, 100),  # Orange
        }
        self.performance_history = []

    def generate_fractal_stress_test(self, depth: int = 5) -> str:
        """Generate recursive comprehensions that create fractal-like patterns"""

        # Fibonacci fractal
        fibonacci_code = f"""
def fibonacci_fractal(n):
    return [fibonacci_fractal(i) for i in range(n) if i < {depth}]
"""

        # Mandelbrot approximation
        mandelbrot_code = f"""
def mandelbrot_approx(x, y, max_iter={depth}):
    c = complex(x, y)
    z = 0
    for i in range(max_iter):
        if abs(z) > 2:
            return i
        z = z*z + c
    return max_iter
"""

        # Generate the fractal code
        fractal_comprehension = f"[mandelbrot_approx(x/100, y/100) for x in range({depth * 20}) for y in range({depth * 20})]"

        return f"{fibonacci_code}\n{mandelbrot_code}\nresult = {fractal_comprehension}"

    def map_performance_to_color(
        self, backend: str, latency: float, throughput: float
    ) -> Tuple[int, int, int]:
        """Map backend performance to color frequencies"""

        base_color = self.color_map.get(backend, (128, 128, 128))

        # Latency affects brightness (higher latency = dimmer)
        brightness_factor = max(0.1, 1.0 - (latency / 1000.0))  # Normalize to 0-1

        # Throughput affects saturation (higher throughput = more saturated)
        saturation_factor = min(1.0, throughput / 100.0)  # Normalize to 0-1

        # Apply factors
        r = int(base_color[0] * brightness_factor * saturation_factor)
        g = int(base_color[1] * brightness_factor * saturation_factor)
        b = int(base_color[2] * brightness_factor * saturation_factor)

        return (r, g, b)

    def generate_particle_system(self, performance_data: Dict) -> List[Dict]:
        """Generate particle system based on performance metrics"""

        particles = []

        for backend, metrics in performance_data.items():
            color = self.map_performance_to_color(
                backend, metrics.get("latency", 0), metrics.get("throughput", 0)
            )

            # Number of particles based on throughput
            particle_count = int(metrics.get("throughput", 0) / 10)

            for _ in range(particle_count):
                particle = {
                    "x": random.uniform(0, 1000),
                    "y": random.uniform(0, 1000),
                    "vx": random.uniform(-5, 5),
                    "vy": random.uniform(-5, 5),
                    "color": color,
                    "size": max(
                        1, metrics.get("latency", 0) / 100
                    ),  # Size based on latency
                    "life": 1.0,
                }
                particles.append(particle)

        return particles

    def generate_fluid_choke_visualization(
        self, error_rate: float, throughput: float
    ) -> Dict:
        """Generate fluid dynamics visualization based on system health"""

        # Fluid speed based on throughput
        fluid_speed = min(10.0, throughput / 10.0)

        # Viscosity based on error rate (higher errors = more viscous)
        viscosity = 1.0 + (error_rate * 10.0)

        # Turbulence based on error rate
        turbulence = error_rate * 5.0

        return {
            "fluid_speed": fluid_speed,
            "viscosity": viscosity,
            "turbulence": turbulence,
            "choke_factor": error_rate,  # 0 = smooth, 1 = completely choked
            "color": (255, int(255 * (1 - error_rate)), int(255 * (1 - error_rate))),
        }

    def generate_swarm_chaos(self, system_health: float) -> Dict:
        """Generate boid swarm behavior based on system health"""

        # Cohesion strength (healthy = strong cohesion)
        cohesion_strength = system_health

        # Separation distance (errors = more scattered)
        separation_distance = 50.0 + (1.0 - system_health) * 100.0

        # Alignment strength (healthy = aligned movement)
        alignment_strength = system_health

        return {
            "cohesion_strength": cohesion_strength,
            "separation_distance": separation_distance,
            "alignment_strength": alignment_strength,
            "swarm_size": int(50 * system_health),  # Fewer boids when unhealthy
            "chaos_level": 1.0 - system_health,
        }

    def generate_lolcat_string_fx(self, performance_data: Dict) -> str:
        """Generate lolcat string effects based on performance"""

        # Base lolcat string
        base_string = "Hellooooo!!!"

        # Performance-based transformations
        total_throughput = sum(
            metrics.get("throughput", 0) for metrics in performance_data.values()
        )
        avg_latency = sum(
            metrics.get("latency", 0) for metrics in performance_data.values()
        ) / len(performance_data)

        # Stretch based on throughput
        stretch_factor = min(3.0, total_throughput / 50.0)
        stretched = base_string * int(stretch_factor)

        # Add performance-based effects
        if avg_latency > 500:
            stretched = stretched.upper()  # High latency = SHOUTING
        if total_throughput > 100:
            stretched = stretched + " 🚀"  # High throughput = rocket
        if any(metrics.get("errors", 0) > 0 for metrics in performance_data.values()):
            stretched = stretched + " 😵"  # Errors = dizzy face

        return stretched

    async def run_performance_art_experiment(self):
        """Run the complete performance art experiment"""

        print("🎨 Starting Creative Performance Art Experiment")
        print("=" * 50)

        # 1. Generate fractal stress test
        print("\n1️⃣ Generating Fractal Stress Test...")
        fractal_code = self.generate_fractal_stress_test(depth=3)

        # 2. Run performance tests on different backends
        print("\n2️⃣ Running Performance Tests...")
        performance_data = {}

        backends = ["rust", "go", "julia", "typescript", "python"]

        for backend in backends:
            print(f"   Testing {backend}...")

            # Simulate performance metrics (in real scenario, run actual tests)
            latency = random.uniform(10, 500)  # ms
            throughput = random.uniform(10, 200)  # req/s
            errors = random.randint(0, 5)

            performance_data[backend] = {
                "latency": latency,
                "throughput": throughput,
                "errors": errors,
                "timestamp": time.time(),
            }

            # Map to color
            color = self.map_performance_to_color(backend, latency, throughput)
            print(
                f"   {backend}: latency={latency:.1f}ms, throughput={throughput:.1f}req/s, color=rgb{color}"
            )

        # 3. Generate particle system
        print("\n3️⃣ Generating Particle System...")
        particles = self.generate_particle_system(performance_data)
        print(f"   Generated {len(particles)} particles")

        # 4. Generate fluid visualization
        print("\n4️⃣ Generating Fluid Visualization...")
        total_errors = sum(metrics["errors"] for metrics in performance_data.values())
        total_throughput = sum(
            metrics["throughput"] for metrics in performance_data.values()
        )
        error_rate = total_errors / max(1, total_throughput)

        fluid_viz = self.generate_fluid_choke_visualization(
            error_rate, total_throughput
        )
        print(f"   Fluid speed: {fluid_viz['fluid_speed']:.2f}")
        print(f"   Viscosity: {fluid_viz['viscosity']:.2f}")
        print(f"   Choke factor: {fluid_viz['choke_factor']:.2f}")

        # 5. Generate swarm behavior
        print("\n5️⃣ Generating Swarm Behavior...")
        system_health = 1.0 - error_rate
        swarm = self.generate_swarm_chaos(system_health)
        print(f"   System health: {system_health:.2f}")
        print(f"   Swarm size: {swarm['swarm_size']}")
        print(f"   Chaos level: {swarm['chaos_level']:.2f}")

        # 6. Generate lolcat effects
        print("\n6️⃣ Generating Lolcat Effects...")
        lolcat_string = self.generate_lolcat_string_fx(performance_data)
        print(f"   Lolcat string: {lolcat_string}")

        # 7. Save art data
        print("\n7️⃣ Saving Art Data...")
        art_data = {
            "timestamp": time.time(),
            "performance_data": performance_data,
            "particles": particles,
            "fluid_visualization": fluid_viz,
            "swarm_behavior": swarm,
            "lolcat_string": lolcat_string,
            "fractal_code": fractal_code,
        }

        output_file = Path("performance_art_data.json")
        with open(output_file, "w") as f:
            json.dump(art_data, f, indent=2)

        print(f"   Art data saved to {output_file}")

        # 8. Generate HTML visualization
        print("\n8️⃣ Generating HTML Visualization...")
        self.generate_html_visualization(art_data)

        print("\n🎉 Creative Performance Art Experiment Complete!")
        print("Open 'performance_art_visualization.html' to see the results!")

    def generate_html_visualization(self, art_data: Dict):
        """Generate HTML visualization of the performance art"""

        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Live - Performance Art Visualization</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(45deg, #1a1a1a, #2d2d2d);
            color: #00ff00;
            margin: 0;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .performance-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .performance-card {
            background: rgba(0, 255, 0, 0.1);
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        
        .color-preview {
            width: 100%;
            height: 50px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .particle-canvas {
            width: 100%;
            height: 400px;
            border: 2px solid #00ff00;
            border-radius: 10px;
            background: #000;
        }
        
        .lolcat-display {
            font-size: 24px;
            text-align: center;
            margin: 20px 0;
            padding: 20px;
            background: rgba(255, 0, 255, 0.2);
            border-radius: 10px;
        }
        
        .fluid-viz {
            height: 100px;
            background: linear-gradient(90deg, 
                rgba(0, 255, 0, 0.3) 0%, 
                rgba(255, 0, 0, 0.3) 100%);
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Code Live - Performance Art Visualization</h1>
            <p>Backend performance metrics transformed into visual art</p>
        </div>
        
        <div class="performance-grid">
"""

        # Add performance cards for each backend
        for backend, metrics in art_data["performance_data"].items():
            color = self.map_performance_to_color(
                backend, metrics["latency"], metrics["throughput"]
            )
            html_content += f"""
            <div class="performance-card">
                <h3>{backend.upper()}</h3>
                <div class="color-preview" style="background-color: rgb({color[0]}, {color[1]}, {color[2]});"></div>
                <p>Latency: {metrics["latency"]:.1f}ms</p>
                <p>Throughput: {metrics["throughput"]:.1f} req/s</p>
                <p>Errors: {metrics["errors"]}</p>
            </div>
"""

        html_content += f"""
        </div>
        
        <div class="lolcat-display">
            {art_data["lolcat_string"]}
        </div>
        
        <div class="fluid-viz" style="opacity: {1 - art_data["fluid_visualization"]["choke_factor"]};"></div>
        
        <div class="particle-canvas" id="particleCanvas"></div>
        
        <div style="margin-top: 30px;">
            <h3>System Health: {(1 - art_data["fluid_visualization"]["choke_factor"]):.2f}</h3>
            <p>Swarm Size: {art_data["swarm_behavior"]["swarm_size"]}</p>
            <p>Chaos Level: {art_data["swarm_behavior"]["chaos_level"]:.2f}</p>
        </div>
    </div>
    
    <script>
        // Simple particle animation
        const canvas = document.getElementById('particleCanvas');
        const ctx = canvas.getContext('2d');
        
        const particles = {json.dumps(art_data["particles"][:50])}; // Limit to 50 particles for performance
        
        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            particles.forEach(particle => {{
                particle.x += particle.vx;
                particle.y += particle.vy;
                
                // Bounce off edges
                if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
                if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;
                
                // Draw particle
                ctx.fillStyle = `rgb(${{particle.color[0]}}, ${{particle.color[1]}}, ${{particle.color[2]}})`;
                ctx.beginPath();
                ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                ctx.fill();
            }});
            
            requestAnimationFrame(animate);
        }}
        
        animate();
    </script>
</body>
</html>
"""

        with open("performance_art_visualization.html", "w") as f:
            f.write(html_content)

        print("   HTML visualization generated!")


async def main():
    """Main experiment runner"""
    generator = PerformanceArtGenerator()
    await generator.run_performance_art_experiment()


if __name__ == "__main__":
    print("🎨 Code Live - Creative Performance Art Experiment")
    print("=" * 50)
    print("Turning backend performance metrics into visual art!")
    print()

    asyncio.run(main())
