# Snapshot Embed Snippets
========================

Drop-in snippets for websites, README, and documentation.

## HTML Embed

### Tour Opener Show (Low Intensity)
```html
<!-- ⤵️ paste into any page -->
<iframe src="out/touring/snapshots/tour_opener-low.html" width="960" height="540" loading="lazy"></iframe>
```

### Tour Opener Show (Mid Intensity)
```html
<!-- ⤵️ paste into any page -->
<iframe src="out/touring/snapshots/tour_opener-mid.html" width="960" height="540" loading="lazy"></iframe>
```

### Tour Opener Show (Peak Intensity)
```html
<!-- ⤵️ paste into any page -->
<iframe src="out/touring/snapshots/tour_opener-peak.html" width="960" height="540" loading="lazy"></iframe>
```

## Markdown Embed

### Tour Opener Show (Low Intensity)
```markdown
[![Tour Opener Show - Low Intensity](out/touring/snapshots/tour_opener-low.html)](out/touring/snapshots/tour_opener-low.html)
```

### Tour Opener Show (Mid Intensity)
```markdown
[![Tour Opener Show - Mid Intensity](out/touring/snapshots/tour_opener-mid.html)](out/touring/snapshots/tour_opener-mid.html)
```

### Tour Opener Show (Peak Intensity)
```markdown
[![Tour Opener Show - Peak Intensity](out/touring/snapshots/tour_opener-peak.html)](out/touring/snapshots/tour_opener-peak.html)
```

## README Integration

### Quick Demo Section
```markdown
## 🎭 Live Demo

Experience the Tour Opener Show with different intensity levels:

- **Low Intensity** (Subtle): [Tour Opener - Low](out/touring/snapshots/tour_opener-low.html)
- **Mid Intensity** (Balanced): [Tour Opener - Mid](out/touring/snapshots/tour_opener-mid.html)
- **Peak Intensity** (Maximum): [Tour Opener - Peak](out/touring/snapshots/tour_opener-peak.html)

### Embed in README
```html
<iframe src="out/touring/snapshots/tour_opener-mid.html" width="960" height="540" loading="lazy"></iframe>
```
```

## GitHub Pages Integration

### _config.yml
```yaml
# GitHub Pages configuration
plugins:
  - jekyll-remote-theme

remote_theme: pages-themes/cayman

# Tour Opener Show integration
tour_opener:
  low: "out/touring/snapshots/tour_opener-low.html"
  mid: "out/touring/snapshots/tour_opener-mid.html"
  peak: "out/touring/snapshots/tour_opener-peak.html"
```

### index.md
```markdown
---
layout: default
title: Code Live v0.5 - Touring Rig
---

# Code Live v0.5 - Touring Rig

## 🎭 Live Demo

<iframe src="out/touring/snapshots/tour_opener-mid.html" width="960" height="540" loading="lazy"></iframe>

## 🎛️ Operator Kit

- **FOH Runbook**: [docs/FOH_RUNBOOK.md](docs/FOH_RUNBOOK.md)
- **Operator Pocket Card**: [docs/OPERATOR_POCKET_CARD.md](docs/OPERATOR_POCKET_CARD.md)
- **Release Notes**: [RELEASE_NOTES_v0.5.0.md](RELEASE_NOTES_v0.5.0.md)
```

## CDN Integration

### Static Hosting
```bash
# Upload to CDN
aws s3 cp out/touring/snapshots/ s3://your-bucket/touring/snapshots/ --recursive
aws s3 cp docs/ s3://your-bucket/docs/ --recursive
aws s3 cp profiles/ s3://your-bucket/profiles/ --recursive
```

### CDN URLs
```html
<!-- CDN-hosted embeds -->
<iframe src="https://your-cdn.com/touring/snapshots/tour_opener-mid.html" width="960" height="540" loading="lazy"></iframe>
```

## Social Media Integration

### Twitter/X
```markdown
🎭 Code Live v0.5 - Touring Rig + Operator Kit

Experience the show: https://your-site.com/touring/snapshots/tour_opener-mid.html

#CodeLive #TouringRig #OperatorKit #TextFX
```

### LinkedIn
```markdown
🚀 Code Live v0.5 - Touring Rig + Operator Kit

Complete professional touring rig system with:
- Bulletproof operator kit
- FOH runbook
- Safety rails
- A11y compliance

Demo: https://your-site.com/touring/snapshots/tour_opener-mid.html
```

## Documentation Integration

### API Documentation
```markdown
## 🎭 Tour Opener Show

### Live Demo
<iframe src="out/touring/snapshots/tour_opener-mid.html" width="960" height="540" loading="lazy"></iframe>

### API Endpoints
- `GET /touring/snapshots/tour_opener-low.html` - Low intensity show
- `GET /touring/snapshots/tour_opener-mid.html` - Mid intensity show  
- `GET /touring/snapshots/tour_opener-peak.html` - Peak intensity show
```

## Accessibility Integration

### A11y Badge
```html
<!-- Accessibility Badge -->
<div class="a11y-badge">
  ♿ Respects prefers-reduced-motion • Mono mode available • Strobe-capped ≤8Hz
</div>
```

### A11y Demo
```html
<!-- A11y-compliant demo -->
<iframe src="out/touring/snapshots/tour_opener-low.html" 
        width="960" 
        height="540" 
        loading="lazy"
        title="Tour Opener Show - Low Intensity (A11y Compliant)">
</iframe>
```

## Performance Integration

### Lazy Loading
```html
<!-- Lazy load for performance -->
<iframe src="out/touring/snapshots/tour_opener-mid.html" 
        width="960" 
        height="540" 
        loading="lazy"
        onload="console.log('Tour Opener Show loaded')">
</iframe>
```

### Preload Hints
```html
<!-- Preload for faster loading -->
<link rel="preload" href="out/touring/snapshots/tour_opener-mid.html" as="document">
<iframe src="out/touring/snapshots/tour_opener-mid.html" width="960" height="540" loading="lazy"></iframe>
```

## Mobile Integration

### Responsive Design
```html
<!-- Responsive iframe -->
<div class="responsive-iframe">
  <iframe src="out/touring/snapshots/tour_opener-mid.html" 
          width="100%" 
          height="540" 
          loading="lazy"
          style="max-width: 960px;">
  </iframe>
</div>
```

### Mobile-First CSS
```css
.responsive-iframe {
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
}

.responsive-iframe iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
```

## Analytics Integration

### Google Analytics
```html
<!-- Analytics tracking -->
<iframe src="out/touring/snapshots/tour_opener-mid.html" 
        width="960" 
        height="540" 
        loading="lazy"
        onload="gtag('event', 'iframe_load', {'event_category': 'touring_rig', 'event_label': 'tour_opener_mid'})">
</iframe>
```

### Custom Analytics
```html
<!-- Custom analytics -->
<iframe src="out/touring/snapshots/tour_opener-mid.html" 
        width="960" 
        height="540" 
        loading="lazy"
        onload="analytics.track('touring_rig_demo_viewed', {intensity: 'mid'})">
</iframe>
```

## Security Integration

### CSP Headers
```html
<!-- Content Security Policy -->
<meta http-equiv="Content-Security-Policy" content="frame-src 'self' https://your-cdn.com;">
<iframe src="out/touring/snapshots/tour_opener-mid.html" width="960" height="540" loading="lazy"></iframe>
```

### Sandbox Attributes
```html
<!-- Sandboxed iframe -->
<iframe src="out/touring/snapshots/tour_opener-mid.html" 
        width="960" 
        height="540" 
        loading="lazy"
        sandbox="allow-scripts allow-same-origin">
</iframe>
```

## Usage Examples

### Basic Usage
```html
<!-- Basic embed -->
<iframe src="out/touring/snapshots/tour_opener-mid.html" width="960" height="540" loading="lazy"></iframe>
```

### Advanced Usage
```html
<!-- Advanced embed with all features -->
<iframe src="out/touring/snapshots/tour_opener-mid.html" 
        width="960" 
        height="540" 
        loading="lazy"
        title="Tour Opener Show - Mid Intensity"
        sandbox="allow-scripts allow-same-origin"
        onload="console.log('Tour Opener Show loaded')">
</iframe>
```

### Error Handling
```html
<!-- Error handling -->
<iframe src="out/touring/snapshots/tour_opener-mid.html" 
        width="960" 
        height="540" 
        loading="lazy"
        onerror="console.error('Failed to load Tour Opener Show')"
        onload="console.log('Tour Opener Show loaded successfully')">
</iframe>
```

