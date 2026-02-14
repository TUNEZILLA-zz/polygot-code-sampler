# Site Structure

```
site/
├── index.html          # Navigation hub (start here)
├── dashboard.html      # Performance benchmarks dashboard
├── benchmarks.json    # Benchmark data (used by dashboard)
├── README.md           # This file
├── scripts/            # Symlink to ../scripts (for physics-fx-dropin)
│
├── live/               # Code Live interfaces
│   ├── code-live.html
│   ├── code-live-physics-fx.html
│   ├── code-live-physics-fx-dropin.html
│   ├── code-live-visual-effects.html
│   ├── code-live-webgl-effects.html
│   ├── code-live-techno-creative.html
│   └── code-live-math-visuals.html
│
├── mixer/              # Code Mixer interfaces
│   ├── code-mixer.html
│   ├── code-mixer-prod.html
│   ├── code-mixer-live.html
│   ├── code-mixer-lolcat.html
│   └── code-mixer-api.html
│
├── demos/              # Demo & utility pages
│   ├── playground.html
│   ├── code-studio.html
│   ├── code-performance.html
│   ├── code-motion.html
│   ├── code-daw.html
│   ├── code-audio-simulator.html
│   ├── code-ai-plugins.html
│   └── code-lolcat-fx.html
│
├── valentines/         # Valentine's special
│   └── valentines-physics-fx.html
│
└── data/               # Test/data files
    └── test_benchmarks.json
```

## Quick Start

```bash
python3 server_prod.py
# Open http://localhost:8787/site/
```

## Key URLs

| Page | Path |
|------|------|
| Site index | `/site/` or `/site/index.html` |
| Dashboard | `/site/dashboard.html` |
| Code Live | `/site/live/code-live.html` |
| Code Mixer | `/site/mixer/code-mixer.html` |
| Playground | `/site/demos/playground.html` |
| Valentine's | `/site/valentines/valentines-physics-fx.html` |
