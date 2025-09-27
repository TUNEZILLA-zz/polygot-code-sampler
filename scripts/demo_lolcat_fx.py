#!/usr/bin/env python3
"""
Demo script for Code Live Lolcat FX Rack
Shows the visual glitch FX layer in action
"""

import asyncio
import time

import aiohttp

# Demo configurations
DEMO_CONFIGS = {
    "party_mode": {
        "target": "rust",
        "code": "[x ** 2 for x in range(10)]",
        "parallel": True,
        "preset": "party",
        "stretch": 0.7,
        "echo": 0.6,
        "rainbow": 0.8,
    },
    "glitch_cat": {
        "target": "ts",
        "code": "[x * y for x in range(5) for y in range(5)]",
        "parallel": True,
        "preset": "glitch",
        "glitch_colors": 0.9,
        "ascii_melt": 0.7,
        "random_insert": 0.8,
    },
    "wave_rider": {
        "target": "go",
        "code": "[str(x) for x in range(8)]",
        "parallel": False,
        "preset": "wave",
        "waveform": 0.8,
        "reverb": 0.6,
        "stutter": 0.5,
    },
    "classic_lolcat": {
        "target": "sql",
        "code": "[x for x in range(12) if x % 2 == 0]",
        "parallel": False,
        "preset": "classic",
        "pitch_shift": 0.7,
        "rainbow": 0.6,
        "stretch": 0.4,
    },
}


async def demo_lolcat_fx():
    """Demo the Lolcat FX Rack with different configurations"""
    print("🎛️ Code Live Lolcat FX Rack Demo")
    print("=" * 60)
    print("The Visual Glitch FX Layer for Code/Text Output")
    print("=" * 60)

    # Test local Lolcat FX function first
    print("\n🔧 Testing Local Lolcat FX Function:")
    print("-" * 40)

    try:
        from lolcat_fx import lolcat_fx

        test_texts = ["hello", "Code Live", "Lolcat FX Rack", "Visual Glitch FX Layer"]

        for text in test_texts:
            print(f"\nOriginal: {text}")
            for preset in ["party", "glitch", "wave", "classic"]:
                result = lolcat_fx(text, preset=preset)
                print(f"{preset.capitalize()}: {result}")

        print("\n✅ Local Lolcat FX Function Working!")

    except Exception as e:
        print(f"❌ Local Lolcat FX Function Error: {e}")
        return

    # Test server integration
    print("\n🌐 Testing Server Integration:")
    print("-" * 40)

    server_url = "http://localhost:8791"

    try:
        async with aiohttp.ClientSession() as session:
            # Test health endpoint
            async with session.get(f"{server_url}/health") as response:
                if response.status == 200:
                    health_data = await response.json()
                    print(f"✅ Server Health: {health_data['message']}")
                else:
                    print(f"❌ Server Health Check Failed: {response.status}")
                    return

            # Test each demo configuration
            for config_name, config in DEMO_CONFIGS.items():
                print(f"\n🎛️ Testing {config_name.upper()}:")
                print("-" * 30)

                start_time = time.time()

                async with session.post(
                    f"{server_url}/render/lolcat", json=config
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        duration = time.time() - start_time

                        print(f"✅ Success in {duration * 1000:.2f}ms")
                        print(f"Target: {data['metrics']['target']}")
                        print(f"Code Length: {data['metrics']['code_length']} chars")
                        print(f"FX Applied: {', '.join(data['fx_applied'])}")
                        print(f"Notes: {len(data['notes'])} effects")

                        # Show a preview of the transformed code
                        code_preview = (
                            data["code"][:100] + "..."
                            if len(data["code"]) > 100
                            else data["code"]
                        )
                        print(f"Code Preview: {code_preview}")

                        # Show some notes
                        if data["notes"]:
                            print("FX Notes:")
                            for note in data["notes"][:3]:  # Show first 3 notes
                                print(f"  {note}")

                    else:
                        print(f"❌ Request Failed: {response.status}")
                        error_text = await response.text()
                        print(f"Error: {error_text}")

            print("\n🎉 Lolcat FX Rack Demo Complete!")
            print("=" * 60)

    except aiohttp.ClientConnectorError:
        print("❌ Server not running. Please start the server first:")
        print("python3 server_lolcat_fx.py")
    except Exception as e:
        print(f"❌ Demo Error: {e}")


async def demo_preset_showcase():
    """Showcase different presets"""
    print("\n🎮 Preset Showcase:")
    print("-" * 40)

    presets = {
        "🎉 Party Mode": {
            "description": "Rainbow + Echo + Stretch",
            "effects": ["Stretch", "Echo", "Rainbow Gradient"],
            "use_case": "Perfect for celebratory code transformations",
        },
        "👾 Glitch Cat": {
            "description": "Random Colors + Unicode Melt",
            "effects": ["Glitch Colors", "ASCII Melt", "Random Insert"],
            "use_case": "Ideal for stress testing and chaos mode",
        },
        "🌊 Wave Rider": {
            "description": "Sine Wave Spacing + Fade",
            "effects": ["Waveform", "Reverb", "Stutter"],
            "use_case": "Great for smooth, flowing text transformations",
        },
        "😹 Classic Lolcat": {
            "description": "Random Caps + Rainbow",
            "effects": ["Pitch Shift", "Rainbow Gradient", "Stretch"],
            "use_case": "The original lolcat experience for code",
        },
    }

    for preset_name, preset_info in presets.items():
        print(f"\n{preset_name}")
        print(f"Description: {preset_info['description']}")
        print(f"Effects: {', '.join(preset_info['effects'])}")
        print(f"Use Case: {preset_info['use_case']}")


async def demo_fx_parameters():
    """Demo different FX parameters"""
    print("\n🎛️ FX Parameters Demo:")
    print("-" * 40)

    fx_parameters = {
        "Core FX": {
            "stretch": "Repeats letters (hello → heeelloooooo)",
            "echo": "Trailing spaces + exclamations (hello → hello ! ! !)",
            "pitch_shift": "Random casing (hello → HeLlOooO)",
            "reverb": "Fade-out letters with spacing (hello → h e l l o o o)",
        },
        "Color FX": {
            "rainbow": "Cycles letters through colors",
            "glitch_colors": "Random ANSI colors per character",
            "neon": "Bold + glow simulation (HELLO → 💚H💙E💜L💖L💛O)",
            "invert": "Alternating background/foreground",
        },
        "Spacing FX": {
            "stutter": "Extra spaces between letters (h   e   l   l   o)",
            "waveform": "Letters arranged in sine-wave pattern",
            "cluster": "Random bursts of duplicated letters (hello → heeeelllllllooo)",
        },
        "Chaos FX": {
            "random_insert": "Drops emojis, ASCII art, or symbols (h⚡️e~l🔥l🐍o!!!)",
            "scramble": "Shuffles letters (hello → lhelooo)",
            "ascii_melt": "Overlays with unicode glitch blocks (hȅ̵͔͝l̸̤͎͑lǭ̴̙)",
        },
    }

    for category, parameters in fx_parameters.items():
        print(f"\n{category}:")
        for param, description in parameters.items():
            print(f"  {param}: {description}")


async def main():
    """Main demo function"""
    print("🎛️ Code Live Lolcat FX Rack - Complete Demo")
    print("=" * 60)
    print("Transforming boring text into sparkly stretched-out chaos!")
    print("=" * 60)

    # Run the main demo
    await demo_lolcat_fx()

    # Showcase presets
    await demo_preset_showcase()

    # Demo FX parameters
    await demo_fx_parameters()

    print("\n🎉 Demo Complete!")
    print("=" * 60)
    print("The Visual Glitch FX Layer is ready for Code Live!")
    print("Transform your code output into sparkly chaos! ✨🌈💥")


if __name__ == "__main__":
    asyncio.run(main())
