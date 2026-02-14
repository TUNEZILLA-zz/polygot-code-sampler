#!/usr/bin/env python3
"""
Emoji Art Gallery - Polyglot Code Sampler Edition
Run: python3 scripts/emoji_art.py [name|all|--cycle]
"""

import argparse
import os
import random
import sys
import time

# NO_COLOR: https://no-color.org/
NO_COLOR = bool(os.environ.get("NO_COLOR"))


def _c(code: str) -> str:
    return "" if NO_COLOR else code


# ANSI colors
R = _c("\033[38;5;196m")
P = _c("\033[38;5;213m")
G = _c("\033[38;5;46m")
B = _c("\033[38;5;39m")
Y = _c("\033[38;5;220m")
M = _c("\033[38;5;201m")
W = _c("\033[38;5;255m")
X = _c("\033[0m")


EMOJI_ART = {
    "heart": [
        "    💕 💕     💕 💕    ",
        "  💕     💕 💕     💕  ",
        " 💕       💕       💕  ",
        " 💕                 💕 ",
        "  💕               💕  ",
        "   💕             💕   ",
        "     💕         💕     ",
        "       💕     💕       ",
        "         💕 💕         ",
        "           💕          ",
    ],
    "robot": [
        "        🤖 POLYGLOT BOT 🤖        ",
        "    ┌─────────────────────┐    ",
        "    │  👁️     👁️  │  📡  │    ",
        "    │    ────────    │    ",
        "    │   💬  ▢  💬   │    ",
        "    └─────────────────────┘    ",
        "    🔧 Python → Rust → TS 🔧    ",
        "    ⚡ 6 targets · 1 intent ⚡   ",
    ],
    "rocket": [
        "           🚀           ",
        "          /|\\          ",
        "         / | \\         ",
        "        /  |  \\        ",
        "       🔥  |  🔥       ",
        "      ✨✨✨|✨✨✨      ",
        "     ═════|═════      ",
        "        pcs --code     ",
        "    \"[x*x for x in range(10)]\"  ",
    ],
    "cat": [
        "    =^.^=     =^.^=    ",
        "   (  o  )   (  o  )   ",
        "    > ^ <       > ^ <  ",
        "   /     \\     /     \\  ",
        "  🐾     🐾   🐾     🐾 ",
        "  lolcat mode: ON 🎨  ",
    ],
    "fire": [
        "        🔥 🔥 🔥        ",
        "      🔥   🔥   🔥      ",
        "    🔥  ⚡  🔥  ⚡  🔥    ",
        "      🔥   🔥   🔥      ",
        "    ⚡   🔥 🔥 🔥   ⚡   ",
        "  ─── PARALLEL SPEED ─── ",
    ],
    "matrix": [
        "  📜 Python   →  🦀 Rust    ",
        "  📜 Python   →  📱 TypeScript",
        "  📜 Python   →  🗄️ SQL     ",
        "  📜 Python   →  🔬 Julia   ",
        "  📜 Python   →  ⚡ Go      ",
        "  📜 Python   →  💎 C#      ",
        "  ═══════════════════════  ",
        "  Write once → Run anywhere  ",
    ],
    "celebration": [
        "  🎉  🎊  ✨  🎉  🎊  ✨  ",
        "     💯  PASSING  💯     ",
        "  ✨  🎊  🎉  ✨  🎊  🎉  ",
        "   polyglot-code-sampler  ",
        "  🎉  ✨  🎊  🎉  ✨  🎊  ",
    ],
    "valentine": [
        "  ❤️  💕  💖  💗  💓  💝  ",
        "  💘  Happy Valentine's  💘  ",
        "  💞  [x for x in love]  💞  ",
        "  ❤️  💕  💖  💗  💓  💝  ",
    ],
}


def show(name: str | None = None) -> str:
    """Display emoji art by name or random."""
    names = list(EMOJI_ART.keys())
    key = name if name and name in EMOJI_ART else random.choice(names)
    art = EMOJI_ART[key]
    colors = [R, P, G, B, Y, M, W]
    print()
    for i, line in enumerate(art):
        c = colors[i % len(colors)]
        print(f"  {c}{line}{X}")
    print()
    return key


def show_all() -> None:
    """Display all emoji art."""
    print(f"\n  {Y}═══ EMOJI ART GALLERY ═══{X}\n")
    for name in EMOJI_ART:
        print(f"  {P}▸ {name}{X}")
        for line in EMOJI_ART[name]:
            print(f"    {line}")
        print()


def cycle(delay: float = 2.0) -> None:
    """Cycle through all emoji art with a delay."""
    names = list(EMOJI_ART.keys())
    clear = "" if NO_COLOR else "\033[2J\033[H"
    try:
        while True:
            for name in names:
                if clear:
                    print(clear, end="")
                print(f"\n  {Y}─── {name} ───{X}\n")
                for line in EMOJI_ART[name]:
                    print(f"  {line}")
                print(f"\n  {P}(Ctrl+C to stop · {delay}s){X}\n")
                sys.stdout.flush()
                time.sleep(delay)
    except KeyboardInterrupt:
        print("\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Display emoji art from the Polyglot Code Sampler gallery",
    )
    parser.add_argument(
        "name",
        nargs="?",
        default=None,
        metavar="name",
        help="Art name: " + ", ".join(EMOJI_ART.keys()) + ", all, or list",
    )
    parser.add_argument(
        "-c", "--cycle",
        action="store_true",
        help="Cycle through all art (Ctrl+C to stop)",
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=2.0,
        help="Delay between slides in cycle mode (default: 2.0)",
    )
    args = parser.parse_args()

    if args.cycle:
        cycle(delay=args.delay)
        return

    name = (args.name or "").lower()
    if name in ("all", "list"):
        show_all()
        return

    if name and name in EMOJI_ART:
        show(name)
        return

    if name and name not in EMOJI_ART:
        print(f"  Unknown art: '{args.name}'")
        print(f"  Available: {', '.join(EMOJI_ART.keys())}\n")
        sys.exit(1)

    show()
    print(f"  Usage: python3 scripts/emoji_art.py [{', '.join(EMOJI_ART.keys())}|all|--cycle]")
    print(f"  Try: python3 scripts/emoji_art.py --help")


if __name__ == "__main__":
    main()
