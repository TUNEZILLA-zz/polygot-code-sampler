#!/usr/bin/env python3
"""
Valentine's Terminal Animation - Polyglot Love Edition
Falling hearts + love-themed code transforms across languages.
Run: python scripts/valentines_terminal.py [duration_sec]
"""

import argparse
import os
import random
import shutil
import sys
import time

# NO_COLOR: https://no-color.org/ - disable ANSI when set
NO_COLOR = bool(os.environ.get("NO_COLOR"))

# ANSI escape codes (empty when NO_COLOR)
def _c(code: str) -> str:
    return "" if NO_COLOR else code

RESET = _c("\033[0m")
DIM = _c("\033[2m")

# Valentine color palette
RED = _c("\033[38;5;196m")
PINK = _c("\033[38;5;213m")
HOT_PINK = _c("\033[38;5;205m")
ROSE = _c("\033[38;5;211m")
WHITE = _c("\033[38;5;255m")
GOLD = _c("\033[38;5;220m")
MAGENTA = _c("\033[38;5;201m")


def ansi_color(text: str, color: str) -> str:
    return f"{color}{text}{RESET}"


def clear_screen() -> None:
    if not NO_COLOR:
        print("\033[2J\033[H", end="")
    else:
        print()


def get_terminal_size() -> tuple[int, int]:
    try:
        size = shutil.get_terminal_size()
        return max(24, size.lines), max(80, size.columns)
    except OSError:
        return 24, 80


# Love-themed code snippets (Python intent → polyglot targets)
LOVE_SNIPPETS = [
    ("Python", "[heart for heart in love if heart.is_true()]", PINK),
    ("Rust", "love.into_par_iter().filter(|h| h.is_true()).collect()", RED),
    ("TypeScript", "love.filter(h => h.isTrue()).map(h => h)", HOT_PINK),
    ("Julia", "[h for h in love if h.is_true()]", MAGENTA),
    ("Go", "filterHearts(love, func(h Heart) bool { return h.IsTrue() })", ROSE),
    ("C#", "love.AsParallel().Where(h => h.IsTrue()).ToList()", GOLD),
    ("SQL", "SELECT * FROM love WHERE is_true = 1", WHITE),
]

HEARTS = ["♥", "💕", "💖", "💗", "💓", "💝", "❤", "💘", "💞"]


def draw_banner(cols: int) -> str:
    """Draw the Valentine's banner."""
    banner = r"""
    __     __   _ _    _       _   _             
    \ \   / /__| | | _(_)_ __ | \ | | ___ _ __  
     \ \ / / _ \ | |/ / | '_ \|  \| |/ _ \ '_ \ 
      \ V /  __/ |   <| | | | | |\  |  __/ | | |
       \_/ \___|_|_|\_\_|_| |_|_| \_|\___|_| |_|
    """
    lines = banner.strip().split("\n")
    centered = []
    for line in lines:
        padding = max(0, (cols - len(line)) // 2)
        centered.append(" " * padding + ansi_color(line, PINK))
    return "\n".join(centered)


def draw_code_snippet(lang: str, code: str, color: str, cols: int) -> str:
    """Draw a single code snippet, truncating to fit terminal width."""
    max_len = cols - 4
    code_trunc = (code[: max_len - 2] + "..") if len(code) > max_len else code
    return "\n".join([
        f"  {ansi_color('→', GOLD)} {ansi_color(lang + ':', DIM)}",
        f"    {color}{code_trunc}{RESET}",
    ])


def run_animation(duration_sec: float = 30, speed: float = 0.08):
    """Run the main animation loop."""
    rows, cols = get_terminal_size()

    # Initialize falling heart columns (spread across width, no overlap)
    num_columns = min(12, (cols - 4) // 8)
    candidates = list(range(2, cols - 2))
    chosen = random.sample(candidates, min(num_columns, len(candidates)))
    column_data = [
        (col, random.randint(3, 8), random.randint(0, 15))
        for col in chosen
    ]

    snippet_idx = 0
    start_time = time.time()
    frame = 0

    try:
        while (time.time() - start_time) < duration_sec:
            clear_screen()

            # Build falling hearts display
            display_rows = rows - 14  # Leave room for banner and code
            if display_rows < 5:
                display_rows = 5

            # Falling hearts: each column drops a trail
            fall_lines = [[" "] * cols for _ in range(display_rows)]
            for col, trail_len, offset in column_data:
                for i in range(trail_len):
                    row_pos = (frame + offset + i) % (display_rows + trail_len + 8)
                    if 0 <= row_pos < display_rows:
                        char = random.choice(HEARTS) if i == 0 else "·"
                        c = min(cols - 1, max(0, col + (frame % 3) - 1))
                        if fall_lines[row_pos][c] == " " or i == 0:
                            color = random.choice([RED, PINK, HOT_PINK, ROSE, MAGENTA])
                            fall_lines[row_pos][c] = f"{color}{char}{RESET}"

            heart_display = "\n".join(["".join(line) for line in fall_lines])

            # Banner
            print(draw_banner(cols))
            print()

            # Code snippet (cycles through languages)
            lang, code, color = LOVE_SNIPPETS[snippet_idx % len(LOVE_SNIPPETS)]
            print(ansi_color("  Write once (Python intent) → compile into many", DIM))
            print(ansi_color("  Polyglot Code Sampler · Valentine's Edition", DIM))
            print()
            print(draw_code_snippet(lang, code, color, cols))
            print()
            print(ansi_color("  " + "♥ " * (cols // 4), PINK))
            print()
            print(heart_display)

            # Footer
            remaining = int(duration_sec - (time.time() - start_time))
            print(ansi_color(f"  Press Ctrl+C to exit · {remaining}s remaining", DIM))

            sys.stdout.flush()

            # Cycle snippet every 3 seconds
            if frame % 40 == 0 and frame > 0:
                snippet_idx += 1

            frame += 1
            time.sleep(speed)

    except KeyboardInterrupt:
        pass

    clear_screen()
    print(ansi_color("\n  Happy Valentine's Day! 💕\n", HOT_PINK))
    print(ansi_color("  pcs --code \"[x for x in love]\" --target rust --parallel", DIM))
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Valentine's terminal animation - falling hearts + polyglot code",
    )
    parser.add_argument(
        "duration",
        nargs="?",
        type=float,
        default=30.0,
        help="Duration in seconds (default: 30)",
    )
    parser.add_argument(
        "-s", "--speed",
        type=float,
        default=0.08,
        help="Frame delay in seconds (default: 0.08)",
    )
    args = parser.parse_args()
    run_animation(duration_sec=args.duration, speed=args.speed)


if __name__ == "__main__":
    main()
