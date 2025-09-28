# Ableton Live → OSC Integration for CodeSampler Live

## Quick Setup Guide

### 1. Install Max for Live OSC Device
- Download and install a Max for Live OSC sender device (e.g., from CNMAT or Shifter M4L pack)
- Or use the built-in "OSC Send" device if available

### 2. Configure OSC Settings
- **Host**: `127.0.0.1`
- **Port**: `57120`
- **Protocol**: UDP

### 3. Track Setup

#### Master Track
- Add "OSC Send" device
- Set Host: `127.0.0.1`, Port: `57120`

#### Automation Lanes
- **Envelope 1**: Map to `/fx/hue` (0..1) — draw ramps synced to song sections
- **Envelope 2**: Map to `/fx/intensity` (0..1) — swells on drops
- **Dummy Clip**: Note C1 at downbeat — route to `/run`

### 4. MIDI Controller Mapping
- **Mod Wheel (CC1)** → `/fx/hue`
- **CC2** → `/fx/intensity`
- **Note C1 (36)** → `/run`

### 5. OSC Address Map
```
/fx/hue <0..1>        → Hue control (0-360°)
/fx/intensity <0..1>  → FX intensity (0-1)
/run                   → Trigger code execution
/crowd/kick            → Audience kick
/gov/cap <0..1>        → FPS governor cap
```

### 6. Usage Examples

#### Basic Control
```
/fx/hue 0.25          # Set hue to 25% (90°)
/fx/intensity 0.8     # Set intensity to 80%
/run                   # Trigger code execution
```

#### Automation Clips
- Create automation clips that send OSC messages
- Sync with your DAW timeline for perfect timing
- Use envelope automation for smooth transitions

#### Live Performance
- Map your MIDI controllers to OSC messages
- Use automation clips for pre-programmed sequences
- Combine with live MIDI control for dynamic performances

### 7. Troubleshooting
- Ensure OSC bridge is running: `make osc-bridge`
- Check firewall settings for port 57120
- Verify OSC device is sending to correct host/port
- Test with TouchOSC or other OSC sender first

### 8. Advanced Setup
- Use multiple OSC devices for different parameters
- Create custom Max for Live devices for specific mappings
- Use MIDI→OSC conversion for hardware controllers
- Set up OSC routing for multiple CodeSampler instances

## Ready for Showtime!
Your Ableton Live setup is now ready to control CodeSampler Live via OSC. Perfect for live performances, studio sessions, and creative coding shows!
