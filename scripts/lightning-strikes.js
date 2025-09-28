/**
 * ⚡ LIGHTNING STRIKES - Beat-Driven Lightning Effects
 * Copy this into your CodeSampler Live sandbox for instant lightning magic!
 */

// ========================================
// ⚡ BEAT-DRIVEN LIGHTNING STRIKES
// ========================================
// Creates dramatic lightning effects on beat
if (ENV.beat && ENV.bands.bass > 0.3) {
  // Create lightning bolt element
  const lightning = document.createElement('div');
  lightning.style.position = 'fixed';
  lightning.style.top = '0';
  lightning.style.left = '0';
  lightning.style.width = '100%';
  lightning.style.height = '100%';
  lightning.style.background = 'linear-gradient(45deg, transparent 30%, white 50%, transparent 70%)';
  lightning.style.pointerEvents = 'none';
  lightning.style.zIndex = '2000';
  lightning.style.opacity = '0.9';
  lightning.style.animation = 'lightning-flash 0.1s ease-out';
  document.body.appendChild(lightning);
  
  // Add CSS animation
  if (!document.getElementById('lightning-styles')) {
    const style = document.createElement('style');
    style.id = 'lightning-styles';
    style.textContent = `
      @keyframes lightning-flash {
        0% { opacity: 0; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); }
        100% { opacity: 0; transform: scale(1); }
      }
    `;
    document.head.appendChild(style);
  }
  
  setTimeout(() => {
    if (document.body.contains(lightning)) {
      document.body.removeChild(lightning);
    }
  }, 150);
}

// ========================================
// 🌩️ BASS-REACTIVE LIGHTNING BOLTS
// ========================================
// Creates lightning bolts that follow bass levels
if (ENV.bands.bass > 0.4) {
  const bolt = document.createElement('div');
  bolt.style.position = 'fixed';
  bolt.style.top = '0';
  bolt.style.left = `${Math.random() * window.innerWidth}px`;
  bolt.style.width = '3px';
  bolt.style.height = '100%';
  bolt.style.background = 'linear-gradient(to bottom, transparent, white, transparent)';
  bolt.style.pointerEvents = 'none';
  bolt.style.zIndex = '1999';
  bolt.style.opacity = ENV.bands.bass;
  bolt.style.boxShadow = '0 0 20px white, 0 0 40px white';
  document.body.appendChild(bolt);
  
  setTimeout(() => {
    if (document.body.contains(bolt)) {
      document.body.removeChild(bolt);
    }
  }, 200);
}

// ========================================
// ⚡ FREQUENCY LIGHTNING STORM
// ========================================
// Creates multiple lightning strikes based on frequency bands
const totalEnergy = ENV.bands.bass + ENV.bands.low + ENV.bands.mid + ENV.bands.high;
if (totalEnergy > 0.5) {
  const strikeCount = Math.floor(totalEnergy * 5);
  
  for (let i = 0; i < strikeCount; i++) {
    const strike = document.createElement('div');
    strike.style.position = 'fixed';
    strike.style.top = '0';
    strike.style.left = `${Math.random() * window.innerWidth}px`;
    strike.style.width = '2px';
    strike.style.height = '100%';
    strike.style.background = 'linear-gradient(to bottom, transparent, white, transparent)';
    strike.style.pointerEvents = 'none';
    strike.style.zIndex = '1998';
    strike.style.opacity = totalEnergy;
    strike.style.boxShadow = '0 0 15px white';
    document.body.appendChild(strike);
    
    setTimeout(() => {
      if (document.body.contains(strike)) {
        document.body.removeChild(strike);
      }
    }, 100 + Math.random() * 100);
  }
}

// ========================================
// 🌈 COLORED LIGHTNING BOLTS
// ========================================
// Creates colorful lightning based on frequency bands
if (ENV.bands.mid > 0.3) {
  const colors = [
    `hsl(${ENV.bands.bass * 360}, 100%, 80%)`,
    `hsl(${ENV.bands.low * 360}, 100%, 80%)`,
    `hsl(${ENV.bands.mid * 360}, 100%, 80%)`,
    `hsl(${ENV.bands.high * 360}, 100%, 80%)`
  ];
  
  const colorIndex = Math.floor(ENV.bands.mid * colors.length);
  const lightningColor = colors[colorIndex];
  
  const coloredBolt = document.createElement('div');
  coloredBolt.style.position = 'fixed';
  coloredBolt.style.top = '0';
  coloredBolt.style.left = `${Math.random() * window.innerWidth}px`;
  coloredBolt.style.width = '4px';
  coloredBolt.style.height = '100%';
  coloredBolt.style.background = `linear-gradient(to bottom, transparent, ${lightningColor}, transparent)`;
  coloredBolt.style.pointerEvents = 'none';
  coloredBolt.style.zIndex = '1997';
  coloredBolt.style.opacity = ENV.bands.mid;
  coloredBolt.style.boxShadow = `0 0 25px ${lightningColor}`;
  document.body.appendChild(coloredBolt);
  
  setTimeout(() => {
    if (document.body.contains(coloredBolt)) {
      document.body.removeChild(coloredBolt);
    }
  }, 300);
}

// ========================================
// ⚡ LIGHTNING STATUS DISPLAY
// ========================================
// Shows lightning strike information
const lightningStatus = document.createElement('div');
lightningStatus.style.position = 'fixed';
lightningStatus.style.top = '20px';
lightningStatus.style.left = '20px';
lightningStatus.style.background = 'rgba(0,0,0,0.8)';
lightningStatus.style.color = 'white';
lightningStatus.style.padding = '10px';
lightningStatus.style.borderRadius = '5px';
lightningStatus.style.fontFamily = 'monospace';
lightningStatus.style.zIndex = '3000';
lightningStatus.style.border = '2px solid #ff6b6b';
document.body.appendChild(lightningStatus);

lightningStatus.innerHTML = `
  <div>⚡ LIGHTNING STRIKES ⚡</div>
  <div>🥁 Beat: ${ENV.beat ? 'YES' : 'NO'}</div>
  <div>🔊 Bass: ${(ENV.bands.bass * 100).toFixed(1)}%</div>
  <div>🎶 Mid: ${(ENV.bands.mid * 100).toFixed(1)}%</div>
  <div>🎵 High: ${(ENV.bands.high * 100).toFixed(1)}%</div>
  <div>⚡ Energy: ${((ENV.bands.bass + ENV.bands.low + ENV.bands.mid + ENV.bands.high) * 100).toFixed(1)}%</div>
  <div>⏰ Time: ${ENV.t.toFixed(1)}s</div>
`;

// ========================================
// 🌩️ LIGHTNING BACKGROUND EFFECT
// ========================================
// Creates a subtle lightning background effect
if (ENV.bands.bass > 0.2) {
  document.body.style.background = `
    linear-gradient(135deg, 
      hsl(${ENV.bands.bass * 360}, 60%, 10%), 
      hsl(${ENV.bands.low * 360}, 60%, 15%),
      hsl(${ENV.bands.mid * 360}, 60%, 20%),
      hsl(${ENV.bands.high * 360}, 60%, 25%)
    )
  `;
}

// ========================================
// ⚡ RETURN LIGHTNING DATA
// ========================================
// Return data for the sandbox display
return {
  time: new Date().toLocaleTimeString(),
  bpm: Math.round(ENV.bpm),
  beat: ENV.beat,
  bass: Number(ENV.bands.bass.toFixed(3)),
  mid: Number(ENV.bands.mid.toFixed(3)),
  high: Number(ENV.bands.high.toFixed(3)),
  lightning: "⚡ LIGHTNING STRIKES ACTIVE! ⚡",
  energy: Number((ENV.bands.bass + ENV.bands.low + ENV.bands.mid + ENV.bands.high).toFixed(3))
};
