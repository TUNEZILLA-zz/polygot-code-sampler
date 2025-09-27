# 🎨 Code Live - Creative Performance Art Experiments

This directory contains experiments that turn backend performance metrics into visual art, creating a unique fusion of technology and creativity.

## 🚀 Quick Start (30 minutes)

### 1. Run the Basic Performance Art Experiment

```bash
# Install dependencies
pip install aiohttp numpy

# Run the creative performance art generator
python3 creative_performance_art.py
```

This will:
- Generate fractal stress tests
- Map backend performance to color frequencies
- Create particle systems based on system health
- Generate fluid dynamics visualizations
- Create lolcat string effects
- Save results to `performance_art_visualization.html`

### 2. Run the Stress Test Art Generator

```bash
# Make sure your server is running on localhost:8000
python3 server.py &

# Run the stress test art generator
python3 stress_test_art.py
```

This will:
- Run a 60-second stress test
- Generate real-time performance art
- Create animated visualizations
- Save results to `stress_test_art_visualization.html`

## 🎨 Creative Experiments

### Fractal Stress Test
- **What**: Recursive comprehensions that create fractal-like patterns
- **Visual**: Nested swirls that mirror fractal growth
- **Creative Lens**: Backend performance = iteration depth → faster backends spawn deeper, sharper fractal visuals

### Color Frequency Spectrum
- **What**: Maps backend performance to color frequencies
- **Visual**: 
  - Rust = low red
  - Go = green  
  - Julia = high violet
  - TypeScript = blue
  - Python = orange
- **Creative Lens**: Backend bottlenecks show up as muddy colors or dim sections

### Physics "Concert" Mode
- **What**: Syncs particle spawns to performance beats
- **Visual**: Particles "pulse" in time with system performance
- **Creative Lens**: Turn stress tests into rhythm visualizers, watching latency spikes as off-beat hiccups

### Fluid "Choke" Visualization
- **What**: Maps throughput to fluid speed and error rate to viscosity
- **Visual**: Fluid "chokes" and "clogs" under errors
- **Creative Lens**: Like a smoke machine sputtering when the system struggles

### Swarm Chaos Game
- **What**: Boid flock cohesion based on system health
- **Visual**: Healthy system = cohesive swarm, errors = scattered chaos
- **Creative Lens**: Interactive art piece where errors = chaos, recovery = harmony

### Lolcat String FX
- **What**: Text transforms that respond to performance
- **Visual**: "Hellooooo!!!" stretches, warps, and bounces with request surges
- **Creative Lens**: Make performance metrics fun and meme-y

## 🎯 Experiment Ideas

### 1. Fractal Depth Test
```python
# Test different recursion depths
depths = [3, 5, 7, 10]
for depth in depths:
    fractal_code = generate_fractal_stress_test(depth)
    # Measure performance and generate art
```

### 2. Color Frequency Mapping
```python
# Map performance metrics to color frequencies
def map_to_color(backend, latency, throughput):
    base_color = color_map[backend]
    brightness = 1.0 - (latency / 1000.0)
    saturation = min(1.0, throughput / 100.0)
    return apply_factors(base_color, brightness, saturation)
```

### 3. Physics Concert Mode
```python
# Sync particles to performance beats
bpm = 120  # beats per minute
beat_interval = 60.0 / bpm
particle_spawns = sync_to_beats(performance_data, beat_interval)
```

### 4. Fluid Choke Test
```python
# Generate fluid dynamics based on system health
fluid_speed = throughput / 10.0
viscosity = 1.0 + (error_rate * 10.0)
turbulence = error_rate * 5.0
```

### 5. Swarm Health Visualization
```python
# Boid behavior based on system health
cohesion_strength = system_health
separation_distance = 50.0 + (1.0 - system_health) * 100.0
alignment_strength = system_health
```

## 🎛️ Customization

### Adding New Backends
```python
color_map = {
    'rust': (255, 100, 100),      # Low red
    'go': (100, 255, 100),        # Green  
    'julia': (200, 100, 255),     # High violet
    'typescript': (100, 200, 255), # Blue
    'python': (255, 200, 100),    # Orange
    'your_backend': (255, 255, 100), # Yellow
}
```

### Custom Art Generators
```python
def generate_custom_art(performance_data):
    # Your custom art generation logic
    return art_data
```

### Custom Visualizations
```python
def generate_custom_html(art_data):
    # Your custom HTML visualization
    return html_content
```

## 🎉 Results

After running the experiments, you'll have:

1. **Performance Art Data**: JSON files with performance metrics and art data
2. **HTML Visualizations**: Interactive web pages showing the art
3. **Particle Systems**: Animated particles responding to performance
4. **Color Mappings**: Visual representation of backend performance
5. **Fluid Dynamics**: System health as fluid behavior
6. **Swarm Behavior**: Collective behavior based on system state

## 🚀 Next Steps

1. **Experiment with different stress patterns**
2. **Add more backends to the color mapping**
3. **Create custom art generators**
4. **Build real-time dashboards**
5. **Integrate with monitoring systems**

## 🎨 Creative Inspiration

- **Fractal Growth**: Use recursion depth as visual complexity
- **Color Harmonies**: Map performance to musical scales
- **Particle Physics**: Use real physics equations for particle behavior
- **Fluid Dynamics**: Implement actual fluid simulation
- **Swarm Intelligence**: Use boid algorithms for collective behavior
- **Lolcat Memes**: Make performance monitoring fun and engaging

---

**Happy Creating! 🎨✨**

Turn your backend performance into art and make monitoring beautiful!
