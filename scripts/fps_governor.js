/**
 * FPS Governor - Auto-throttle system for chaos-grade FX
 * Prevents MacBook crashes by gracefully scaling down intensity
 */

class FPSGovernor {
  constructor() {
    this.targetFPS = 45; // Target FPS for smooth performance
    this.minFPS = 30;   // Minimum FPS before emergency throttle
    this.currentFPS = 60;
    this.frameCount = 0;
    this.lastTime = performance.now();
    this.throttleLevel = 0; // 0 = full power, 1 = 75%, 2 = 50%, 3 = 25%
    this.emergencyMode = false;
    
    this.fpsHistory = [];
    this.maxHistory = 30; // 30 frames of history
    
    this.startMonitoring();
  }
  
  startMonitoring() {
    const monitor = () => {
      this.updateFPS();
      this.adjustThrottle();
      requestAnimationFrame(monitor);
    };
    requestAnimationFrame(monitor);
  }
  
  updateFPS() {
    const now = performance.now();
    const delta = now - this.lastTime;
    this.lastTime = now;
    
    if (delta > 0) {
      this.currentFPS = 1000 / delta;
      this.fpsHistory.push(this.currentFPS);
      
      if (this.fpsHistory.length > this.maxHistory) {
        this.fpsHistory.shift();
      }
    }
  }
  
  getAverageFPS() {
    if (this.fpsHistory.length === 0) return 60;
    return this.fpsHistory.reduce((a, b) => a + b, 0) / this.fpsHistory.length;
  }
  
  adjustThrottle() {
    const avgFPS = this.getAverageFPS();
    
    // Emergency mode: FPS below minimum
    if (avgFPS < this.minFPS && !this.emergencyMode) {
      this.emergencyMode = true;
      this.throttleLevel = 3; // Maximum throttle
      this.triggerEmergencyThrottle();
      return;
    }
    
    // Recovery from emergency
    if (this.emergencyMode && avgFPS > this.minFPS + 10) {
      this.emergencyMode = false;
      this.throttleLevel = Math.max(0, this.throttleLevel - 1);
    }
    
    // Gradual throttle based on performance
    if (avgFPS < this.targetFPS - 5) {
      this.throttleLevel = Math.min(3, this.throttleLevel + 1);
    } else if (avgFPS > this.targetFPS + 5) {
      this.throttleLevel = Math.max(0, this.throttleLevel - 1);
    }
  }
  
  triggerEmergencyThrottle() {
    console.warn('🚨 EMERGENCY THROTTLE ACTIVATED');
    console.warn(`FPS dropped to ${this.getAverageFPS().toFixed(1)} - scaling down to 25%`);
    
    // Dispatch emergency event
    window.dispatchEvent(new CustomEvent('fps-emergency', {
      detail: { throttleLevel: 3, fps: this.getAverageFPS() }
    }));
  }
  
  getThrottleMultiplier() {
    const multipliers = [1.0, 0.75, 0.5, 0.25];
    return multipliers[this.throttleLevel];
  }
  
  getParticleCount(maxParticles) {
    return Math.floor(maxParticles * this.getThrottleMultiplier());
  }
  
  getSpeedMultiplier(baseSpeed) {
    return baseSpeed * this.getThrottleMultiplier();
  }
  
  getDensityMultiplier(baseDensity) {
    return Math.max(0.1, baseDensity * this.getThrottleMultiplier());
  }
  
  getStatus() {
    return {
      fps: this.getAverageFPS(),
      throttleLevel: this.throttleLevel,
      emergencyMode: this.emergencyMode,
      multiplier: this.getThrottleMultiplier()
    };
  }
}

// Global FPS Governor instance
window.FPSGovernor = FPSGovernor;

// Auto-initialize if not already running
if (!window.fpsGovernor) {
  window.fpsGovernor = new FPSGovernor();
  
  // Add status display
  const statusDiv = document.createElement('div');
  statusDiv.id = 'fps-governor-status';
  statusDiv.style.cssText = `
    position: fixed;
    top: 10px;
    right: 10px;
    background: rgba(0,0,0,0.8);
    color: #0f0;
    padding: 8px 12px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 11px;
    z-index: 10000;
    border: 1px solid #0f0;
  `;
  document.body.appendChild(statusDiv);
  
  // Update status display
  setInterval(() => {
    const status = window.fpsGovernor.getStatus();
    const color = status.emergencyMode ? '#f00' : 
                  status.throttleLevel > 0 ? '#ff0' : '#0f0';
    
    statusDiv.style.borderColor = color;
    statusDiv.style.color = color;
    statusDiv.innerHTML = `
      FPS: ${status.fps.toFixed(1)}<br>
      Throttle: ${(status.throttleLevel * 25)}%<br>
      ${status.emergencyMode ? '🚨 EMERGENCY' : '✅ OK'}
    `;
  }, 100);
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = FPSGovernor;
}
