#!/usr/bin/env python3
"""
🎼 Conductor Score CLI - Musical Score for Text Performance
=========================================================

CLI for the Conductor Score DSL:
- [Tremolo forte] TuneZilla [/]
- [Pizzicato piano] Rawtunez [/]
- [Violin Solo crescendo] Code Live [/]
- [Guitar Lead ff neon] Rawtunez [/]
"""

import argparse
import sys
from pathlib import Path

# Add the string_fx directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "string_fx"))

from conductor_score import ConductorScoreRenderer, ConductorScoreComposer
from runtime import FXConfig, OutputMode


def main():
    parser = argparse.ArgumentParser(
        description="🎼 Conductor Score DSL - Musical Score for Text Performance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic score
  python3 scripts/conductor_score_cli.py --score "[Tremolo forte] TuneZilla [/]"

  # Crescendo score
  python3 scripts/conductor_score_cli.py --score "[Violin Solo crescendo] Code Live [/]"

  # Hybrid score
  python3 scripts/conductor_score_cli.py --score "[Guitar Lead ff neon] Rawtunez [/]"

  # Ensemble score
  python3 scripts/conductor_score_cli.py --text "Code Live TuneZilla Rawtunez" --ensemble

  # Crescendo score
  python3 scripts/conductor_score_cli.py --text "Code Live TuneZilla Rawtunez" --crescendo

  # Hybrid score
  python3 scripts/conductor_score_cli.py --text "TuneZilla" --technique "guitar_lead" --hybrid-fx "neon"

  # Create score
  python3 scripts/conductor_score_cli.py --create-score --text "TuneZilla" --technique "violin_solo" --dynamics "ff"
        """
    )
    
    parser.add_argument("--score", "-s", help="Conductor score DSL string")
    parser.add_argument("--text", "-t", help="Input text to transform")
    parser.add_argument("--ensemble", action="store_true", help="Create ensemble score")
    parser.add_argument("--crescendo", action="store_true", help="Create crescendo score")
    parser.add_argument("--create-score", action="store_true", help="Create a conductor score")
    parser.add_argument("--technique", help="Technique for create-score (tremolo, vibrato, violin_solo, etc.)")
    parser.add_argument("--dynamics", help="Dynamics for create-score (pp, p, mp, mf, f, ff, fff)")
    parser.add_argument("--section", help="Section for create-score (violins, violas, cellos, basses)")
    parser.add_argument("--hybrid-fx", help="Hybrid FX for create-score (neon, glitch, rainbow, stutter, scramble)")
    parser.add_argument("--intensity", "-i", type=float, default=0.75, help="Intensity knob (0.0-1.0)")
    parser.add_argument("--seed", type=int, help="Seed for deterministic effects")
    parser.add_argument("--mode", "-m", choices=["raw", "ansi", "html"], default="ansi", help="Output mode")
    parser.add_argument("--output", "-o", help="Output file (for HTML mode)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Create FX config
    config = FXConfig(
        intensity=args.intensity,
        seed=args.seed,
        mode=OutputMode(args.mode),
        max_length=8000,
        budget_ms=100
    )
    
    renderer = ConductorScoreRenderer()
    composer = ConductorScoreComposer()
    
    if args.create_score:
        # Create a conductor score
        if not args.text or not args.technique:
            print("❌ Must specify --text and --technique for create-score")
            return
        
        score = composer.create_score(
            args.text, 
            args.technique, 
            args.dynamics or "mf",
            args.section,
            False,  # crescendo
            False,  # decrescendo
            args.hybrid_fx
        )
        
        print(f"🎼 Created Score: {score}")
        
        if args.verbose:
            print(f"📝 Text: {args.text}")
            print(f"🎵 Technique: {args.technique}")
            print(f"🔊 Dynamics: {args.dynamics or 'mf'}")
            if args.section:
                print(f"🎻 Section: {args.section}")
            if args.hybrid_fx:
                print(f"🎨 Hybrid FX: {args.hybrid_fx}")
            print()
        
        # Render the score
        result = renderer.render(score, config)
        print(f"🎼 Result: {result}")
        
    elif args.ensemble:
        # Create ensemble score
        if not args.text:
            print("❌ Must specify --text for ensemble")
            return
        
        score = composer.create_ensemble_score(args.text)
        print(f"🎼 Ensemble Score: {score}")
        
        if args.verbose:
            print(f"📝 Text: {args.text}")
            print(f"🎻 Ensemble: violins, violas, cellos, basses")
            print()
        
        # Render the score
        result = renderer.render(score, config)
        print(f"🎼 Ensemble Result: {result}")
        
    elif args.crescendo:
        # Create crescendo score
        if not args.text:
            print("❌ Must specify --text for crescendo")
            return
        
        score = composer.create_crescendo_score(args.text)
        print(f"🎼 Crescendo Score: {score}")
        
        if args.verbose:
            print(f"📝 Text: {args.text}")
            print(f"📈 Crescendo: p → mp → mf → f → ff")
            print()
        
        # Render the score
        result = renderer.render(score, config)
        print(f"🎼 Crescendo Result: {result}")
        
    elif args.score:
        # Render existing score
        if args.verbose:
            print(f"🎼 Conductor Score DSL - Musical Score for Text Performance")
            print(f"==========================================================")
            print(f"📝 Score: {args.score}")
            print(f"⚙️  Intensity: {args.intensity}")
            if args.seed:
                print(f"🎲 Seed: {args.seed}")
            print(f"📱 Mode: {args.mode}")
            print()
        
        result = renderer.render(args.score, config)
        
        if args.output and args.mode == "html":
            # Create HTML output
            html_content = create_html_output(result, args.score, config)
            with open(args.output, 'w') as f:
                f.write(html_content)
            print(f"🌐 HTML output saved to: {args.output}")
        else:
            print(result)
        
        if args.verbose:
            print(f"🎼 Conductor Score complete!")
            
    else:
        print("❌ Must specify --score, --ensemble, --crescendo, or --create-score")
        return


def create_html_output(result: str, score: str, config: FXConfig) -> str:
    """Create HTML output with styling"""
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎼 Conductor Score Output</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: #000;
            color: #fff;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .title {{
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #ff00ff, #00ffff, #ffff00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .subtitle {{
            color: #888;
            font-size: 1.2em;
        }}
        .output {{
            background: #111;
            border: 2px solid #333;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            font-size: 1.5em;
            line-height: 1.6;
            word-wrap: break-word;
        }}
        .info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .info-item {{
            background: #222;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #00ffff;
        }}
        .info-label {{
            color: #00ffff;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .info-value {{
            color: #fff;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }}
        .copy-btn {{
            background: #00ffff;
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            margin: 10px;
        }}
        .copy-btn:hover {{
            background: #00cccc;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">🎼 Conductor Score Output</h1>
            <p class="subtitle">Musical Score for Text Performance</p>
        </div>
        
        <div class="output">
            {result}
        </div>
        
        <div class="info">
            <div class="info-item">
                <div class="info-label">Score</div>
                <div class="info-value">{score}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Intensity</div>
                <div class="info-value">{config.intensity}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Seed</div>
                <div class="info-value">{config.seed or 'Random'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Mode</div>
                <div class="info-value">{config.mode.value}</div>
            </div>
        </div>
        
        <div style="text-align: center;">
            <button class="copy-btn" onclick="copyToClipboard()">📋 Copy Output</button>
            <button class="copy-btn" onclick="copyAsMarkdown()">📝 Copy as Markdown</button>
        </div>
        
        <div class="footer">
            <p>Generated by Conductor Score DSL</p>
            <p>Score: {score} | Intensity: {config.intensity} | Seed: {config.seed or 'Random'}</p>
        </div>
    </div>
    
    <script>
        function copyToClipboard() {{
            navigator.clipboard.writeText(`{result}`).then(() => {{
                alert('Output copied to clipboard!');
            }});
        }}
        
        function copyAsMarkdown() {{
            const markdown = `# Conductor Score Output\\n\\n**Score:** {score}\\n\\n**Result:**\\n\\n\`\`\`\\n{result}\\n\`\`\`\\n\\n**Intensity:** {config.intensity}\\n**Seed:** {config.seed or 'Random'}`;
            navigator.clipboard.writeText(markdown).then(() => {{
                alert('Markdown copied to clipboard!');
            }});
        }}
    </script>
</body>
</html>
    """
    
    return html


if __name__ == "__main__":
    main()
