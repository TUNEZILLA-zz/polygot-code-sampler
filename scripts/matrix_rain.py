#!/usr/bin/env python3
"""
Matrix Rain Effect - Cmatrix-style animated text rain
Perfect for chaos concert visual effects!
"""

import time
import random
import sys
import os
from typing import List, Tuple
import argparse

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MatrixRain:
    def __init__(self, width: int = 80, height: int = 24, speed: float = 0.1):
        self.width = width
        self.height = height
        self.speed = speed
        self.matrix = [[" " for _ in range(width)] for _ in range(height)]
        self.drops = []
        self.chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
        self.colors = [
            "\033[32m",  # Green
            "\033[36m",  # Cyan
            "\033[33m",  # Yellow
            "\033[35m",  # Magenta
            "\033[31m",  # Red
            "\033[34m",  # Blue
        ]
        self.reset = "\033[0m"

    def init_drops(self):
        """Initialize rain drops"""
        for x in range(self.width):
            if random.random() < 0.3:  # 30% chance to start a drop
                self.drops.append(
                    {
                        "x": x,
                        "y": 0,
                        "speed": random.uniform(0.5, 2.0),
                        "char": random.choice(self.chars),
                        "color": random.choice(self.colors),
                        "brightness": 1.0,
                    }
                )

    def update_drops(self):
        """Update all rain drops"""
        for drop in self.drops[:]:
            # Move drop down
            drop["y"] += drop["speed"] * self.speed

            # Fade brightness
            drop["brightness"] *= 0.98

            # Remove if off screen or too dim
            if drop["y"] >= self.height or drop["brightness"] < 0.1:
                self.drops.remove(drop)
                # Maybe spawn new drop
                if random.random() < 0.1:
                    self.drops.append(
                        {
                            "x": random.randint(0, self.width - 1),
                            "y": 0,
                            "speed": random.uniform(0.5, 2.0),
                            "char": random.choice(self.chars),
                            "color": random.choice(self.colors),
                            "brightness": 1.0,
                        }
                    )

    def render_matrix(self):
        """Render the matrix to screen"""
        # Clear screen
        print("\033[2J\033[H", end="")

        # Clear matrix
        for y in range(self.height):
            for x in range(self.width):
                self.matrix[y][x] = " "

        # Draw drops
        for drop in self.drops:
            x, y = int(drop["x"]), int(drop["y"])
            if 0 <= x < self.width and 0 <= y < self.height:
                # Create trail effect
                trail_length = int(drop["brightness"] * 8)
                for i in range(trail_length):
                    trail_y = y - i
                    if 0 <= trail_y < self.height:
                        char = drop["char"] if i == 0 else random.choice(self.chars)
                        self.matrix[trail_y][x] = char

        # Print matrix
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                char = self.matrix[y][x]
                if char != " ":
                    # Find the drop for this position to get color
                    color = "\033[32m"  # Default green
                    brightness = 1.0
                    for drop in self.drops:
                        if int(drop["x"]) == x and int(drop["y"]) == y:
                            color = drop["color"]
                            brightness = drop["brightness"]
                            break

                    # Apply brightness
                    if brightness < 0.3:
                        color = "\033[90m"  # Dim
                    elif brightness < 0.6:
                        color = "\033[37m"  # Bright

                    line += f"{color}{char}{self.reset}"
                else:
                    line += " "
            print(line)

    def run(self, duration: float = 30.0):
        """Run the matrix rain effect"""
        self.init_drops()
        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                self.update_drops()
                self.render_matrix()
                time.sleep(self.speed)
        except KeyboardInterrupt:
            pass
        finally:
            # Clear screen and reset
            print("\033[2J\033[H\033[0m", end="")


def main():
    parser = argparse.ArgumentParser(
        description="Matrix Rain Effect - Cmatrix-style animated text rain"
    )
    parser.add_argument(
        "--width", type=int, default=80, help="Matrix width (default: 80)"
    )
    parser.add_argument(
        "--height", type=int, default=24, help="Matrix height (default: 24)"
    )
    parser.add_argument(
        "--speed", type=float, default=0.1, help="Animation speed (default: 0.1)"
    )
    parser.add_argument(
        "--duration", type=float, default=30.0, help="Duration in seconds (default: 30)"
    )
    parser.add_argument("--output", type=str, help="Output HTML file")

    args = parser.parse_args()

    if args.output:
        # Generate HTML version
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matrix Rain Effect - Chaos Concert</title>
    <style>
        body {{
            background: #000;
            color: #0f0;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
            overflow: hidden;
        }}
        .matrix-container {{
            position: relative;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
        }}
        .matrix-char {{
            position: absolute;
            color: #0f0;
            font-size: 14px;
            line-height: 1;
            animation: fade 2s linear infinite;
        }}
        @keyframes fade {{
            0% {{ opacity: 1; color: #0f0; }}
            50% {{ opacity: 0.7; color: #0a0; }}
            100% {{ opacity: 0.1; color: #050; }}
        }}
        .title {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 48px;
            color: #0f0;
            text-shadow: 0 0 20px #0f0;
            z-index: 10;
            animation: pulse 2s ease-in-out infinite alternate;
        }}
        @keyframes pulse {{
            from {{ text-shadow: 0 0 20px #0f0; }}
            to {{ text-shadow: 0 0 40px #0f0, 0 0 60px #0f0; }}
        }}
    </style>
</head>
<body>
    <div class="matrix-container">
        <div class="title">CHAOS CONCERT</div>
        <div id="matrix"></div>
    </div>
    
    <script>
        const chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン";
        const colors = ['#0f0', '#0a0', '#050', '#0f0', '#0a0', '#050'];
        const matrix = document.getElementById('matrix');
        const width = {args.width};
        const height = {args.height};
        const speed = {args.speed};
        
        let drops = [];
        
        function initDrops() {{
            for (let x = 0; x < width; x++) {{
                if (Math.random() < 0.3) {{
                    drops.push({{
                        x: x,
                        y: 0,
                        speed: Math.random() * 1.5 + 0.5,
                        char: chars[Math.floor(Math.random() * chars.length)],
                        color: colors[Math.floor(Math.random() * colors.length)],
                        brightness: 1.0
                    }});
                }}
            }}
        }}
        
        function updateDrops() {{
            drops = drops.filter(drop => {{
                drop.y += drop.speed * speed;
                drop.brightness *= 0.98;
                return drop.y < height && drop.brightness > 0.1;
            }});
            
            // Spawn new drops
            if (Math.random() < 0.1) {{
                drops.push({{
                    x: Math.floor(Math.random() * width),
                    y: 0,
                    speed: Math.random() * 1.5 + 0.5,
                    char: chars[Math.floor(Math.random() * chars.length)],
                    color: colors[Math.floor(Math.random() * colors.length)],
                    brightness: 1.0
                }});
            }}
        }}
        
        function renderMatrix() {{
            matrix.innerHTML = '';
            
            drops.forEach(drop => {{
                const x = Math.floor(drop.x);
                const y = Math.floor(drop.y);
                
                if (x >= 0 && x < width && y >= 0 && y < height) {{
                    const char = document.createElement('div');
                    char.className = 'matrix-char';
                    char.textContent = drop.char;
                    char.style.left = (x * 14) + 'px';
                    char.style.top = (y * 14) + 'px';
                    char.style.color = drop.color;
                    char.style.opacity = drop.brightness;
                    matrix.appendChild(char);
                }}
            }});
        }}
        
        function animate() {{
            updateDrops();
            renderMatrix();
            requestAnimationFrame(animate);
        }}
        
        initDrops();
        animate();
    </script>
</body>
</html>
        """

        with open(args.output, "w") as f:
            f.write(html_content)
        print(f"✅ Matrix Rain HTML saved to: {args.output}")
    else:
        # Run terminal version
        matrix = MatrixRain(args.width, args.height, args.speed)
        matrix.run(args.duration)


if __name__ == "__main__":
    main()
