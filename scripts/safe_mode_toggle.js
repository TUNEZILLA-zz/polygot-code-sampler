/**
 * Safe Mode Toggle - ⌘+Shift+S hotkey for emergency safety
 * Instantly scales down all FX to MacBook-safe levels
 */

class SafeModeToggle {
  constructor() {
    this.safeMode = false;
    this.originalSettings = {};
    this.setupHotkey();
    this.setupUI();
  }
  
  setupHotkey() {
    document.addEventListener('keydown', (e) => {
      // ⌘+Shift+S (Cmd+Shift+S on Mac)
      if (e.metaKey && e.shiftKey && e.key === 'S') {
        e.preventDefault();
        this.toggleSafeMode();
      }
    });
  }
  
  setupUI() {
    // Create safe mode indicator
    const indicator = document.createElement('div');
    indicator.id = 'safe-mode-indicator';
    indicator.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(255, 0, 0, 0.9);
      color: white;
      padding: 20px 40px;
      border-radius: 8px;
      font-family: monospace;
      font-size: 18px;
      font-weight: bold;
      z-index: 20000;
      border: 3px solid #fff;
      box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
      display: none;
      text-align: center;
    `;
    indicator.innerHTML = `
      🛡️ SAFE MODE ACTIVATED<br>
      <small>Press ⌘+Shift+S to disable</small>
    `;
    document.body.appendChild(indicator);
  }
  
  toggleSafeMode() {
    this.safeMode = !this.safeMode;
    
    if (this.safeMode) {
      this.activateSafeMode();
    } else {
      this.deactivateSafeMode();
    }
    
    this.showIndicator();
  }
  
  activateSafeMode() {
    console.log('🛡️ SAFE MODE ACTIVATED - Scaling down all FX');
    
    // Store original settings
    this.originalSettings = {
      particleCount: window.cfg?.max || 1000,
      speed: window.SPEED || 1.0,
      density: window.DENS || 0.7,
      reduced: window.REDUCED || false
    };
    
    // Apply safe mode settings
    if (window.cfg) window.cfg.max = Math.floor(this.originalSettings.particleCount * 0.25);
    if (window.SPEED !== undefined) window.SPEED = 0.5;
    if (window.DENS !== undefined) window.DENS = 0.3;
    if (window.REDUCED !== undefined) window.REDUCED = true;
    
    // Force reduced motion
    document.body.classList.add('reduced-motion');
    
    // Dispatch safe mode event
    window.dispatchEvent(new CustomEvent('safe-mode-activated', {
      detail: { 
        particleCount: window.cfg?.max,
        speed: window.SPEED,
        density: window.DENS
      }
    }));
  }
  
  deactivateSafeMode() {
    console.log('🚀 SAFE MODE DEACTIVATED - Restoring full power');
    
    // Restore original settings
    if (window.cfg) window.cfg.max = this.originalSettings.particleCount;
    if (window.SPEED !== undefined) window.SPEED = this.originalSettings.speed;
    if (window.DENS !== undefined) window.DENS = this.originalSettings.density;
    if (window.REDUCED !== undefined) window.REDUCED = this.originalSettings.reduced;
    
    // Remove reduced motion
    document.body.classList.remove('reduced-motion');
    
    // Dispatch safe mode event
    window.dispatchEvent(new CustomEvent('safe-mode-deactivated', {
      detail: { 
        particleCount: window.cfg?.max,
        speed: window.SPEED,
        density: window.DENS
      }
    }));
  }
  
  showIndicator() {
    const indicator = document.getElementById('safe-mode-indicator');
    if (!indicator) return;
    
    indicator.style.display = 'block';
    
    setTimeout(() => {
      indicator.style.display = 'none';
    }, 2000);
  }
  
  isSafeMode() {
    return this.safeMode;
  }
  
  getSafeSettings() {
    return {
      particleCount: Math.floor((window.cfg?.max || 1000) * 0.25),
      speed: 0.5,
      density: 0.3,
      reduced: true
    };
  }
}

// Global Safe Mode Toggle instance
window.SafeModeToggle = SafeModeToggle;

// Auto-initialize
if (!window.safeModeToggle) {
  window.safeModeToggle = new SafeModeToggle();
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SafeModeToggle;
}
