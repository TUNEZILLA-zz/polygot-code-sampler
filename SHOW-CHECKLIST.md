# 🎭 CodeSampler Live - Show Checklist

## 🚀 Pre-Show Setup (30 minutes before doors)

### 1. System Startup
```bash
# Start all services
pm2 resurrect
# OR
pm2 start ecosystem.config.cjs

# Check status
pm2 status
pm2 logs
```

### 2. Health Checks
```bash
# Run smoke tests
node scripts/smoke-tests.js

# Manual checks
curl -I http://localhost:5173/crowd/
```

### 3. Crowd UI Setup
- [ ] Open `/crowd/` on your phone
- [ ] Enter PIN: `9462`
- [ ] Verify status bar shows live data (FPS/Cap/Gov/BPM)
- [ ] Test scene presets (chill/bloom/club/matrix)
- [ ] Test governor cap slider

### 4. QR Code for Audience
```bash
make qr-share
# Put QR code on projector/screen
```

### 5. DAW Integration (Ableton)
- [ ] Load Max for Live device: `scripts/m4l/osc_sender.maxpat`
- [ ] Test OSC routes: `/fx/hue`, `/fx/intensity`, `/run`, `/gov/cap`
- [ ] Map CC1/CC2 to your controller
- [ ] Test C1 note for `/run` trigger

### 6. Visual Demo Test
- [ ] Load "Downbeat Bloom" demo in CodeSampler
- [ ] Play 10-second bass hit
- [ ] Verify visual response and particle bursts
- [ ] Check FPS stays 50-60 (governor working)

## 🎛️ Show-Time Monitoring

### FOH Controls
- **Scene Presets:** Instant mood changes
- **Governor Cap:** Live FPS management (0-1)
- **Status Bar:** Real-time performance metrics
- **Crowd Participation:** Audience can nudge/control

### Performance Metrics
- **FPS:** Green (≥55), Yellow (45-54), Red (<45)
- **Particle Cap:** Current count vs max
- **BPM:** Live tempo detection
- **Governor:** Auto vs override status

## 🧯 Troubleshooting

### Crowd UI Issues
```bash
# Check WebSocket connection
pm2 logs crowd-server

# Restart crowd server
pm2 restart crowd-server
```

### OSC Not Working
```bash
# Check OSC bridge
pm2 logs osc-bridge

# Test with oscsend
oscsend 127.0.0.1 57120 /fx/hue f 0.5
```

### Low FPS
- Lower Governor Cap slider (e.g., 0.45)
- Reduce demo intensity
- Check system resources: `pm2 monit`

### CORS/Origin Issues
- Clear `CROWD_ORIGIN` in `.env`
- Or set to your public URL

### Mic/BPM Stuck
- Check browser mic permissions
- Refresh page
- Verify audio input selected

## 🔄 Rollback Plan

```bash
# List available versions
git tag --list

# Rollback to previous version
git checkout v0.9.0
pm2 restart app osc-bridge crowd-server
```

## 📊 Post-Show

### Logs Export
```bash
# Export logs for analysis
pm2 logs > show-logs-$(date +%Y%m%d).txt
```

### Performance Data
- FPS graphs from status bar
- Crowd participation metrics
- OSC message counts

## 🎭 Pro Tips

1. **Backup Device:** Keep second laptop running same setup
2. **Network:** Use dedicated router/AP for stability
3. **Power:** UPS for critical equipment
4. **Testing:** Run full show flow 1 hour before doors
5. **Documentation:** Keep this checklist handy

---

**🌙✨ Ready for epic live coding performances! 🚀🎭**
