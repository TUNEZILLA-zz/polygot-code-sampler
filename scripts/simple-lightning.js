/**
 * ⚡ SIMPLE LIGHTNING STRIKES - Easy Copy & Paste
 * Copy this into your CodeSampler Live sandbox for instant lightning!
 */

// ⚡ BEAT-DRIVEN LIGHTNING FLASH
if (ENV.beat && ENV.bands.bass > 0.3) {
  document.body.style.filter = 'brightness(3) contrast(2)';
  setTimeout(() => {
    document.body.style.filter = 'none';
  }, 100);
}

// 🌩️ BASS-REACTIVE LIGHTNING BOLTS
if (ENV.bands.bass > 0.4) {
  const bolt = document.createElement('div');
  bolt.style.position = 'fixed';
  bolt.style.top = '0';
  bolt.style.left = Math.random() * window.innerWidth + 'px';
  bolt.style.width = '3px';
  bolt.style.height = '100%';
  bolt.style.background = 'linear-gradient(to bottom, transparent, white, transparent)';
  bolt.style.pointerEvents = 'none';
  bolt.style.zIndex = '2000';
  bolt.style.opacity = ENV.bands.bass;
  bolt.style.boxShadow = '0 0 20px white';
  document.body.appendChild(bolt);
  
  setTimeout(() => {
    if (document.body.contains(bolt)) {
      document.body.removeChild(bolt);
    }
  }, 200);
}

// ⚡ FREQUENCY LIGHTNING STORM
const totalEnergy = ENV.bands.bass + ENV.bands.low + ENV.bands.mid + ENV.bands.high;
if (totalEnergy > 0.5) {
  const strikeCount = Math.floor(totalEnergy * 5);
  
  for (let i = 0; i < strikeCount; i++) {
    const strike = document.createElement('div');
    strike.style.position = 'fixed';
    strike.style.top = '0';
    strike.style.left = Math.random() * window.innerWidth + 'px';
    strike.style.width = '2px';
    strike.style.height = '100%';
    strike.style.background = 'linear-gradient(to bottom, transparent, white, transparent)';
    strike.style.pointerEvents = 'none';
    strike.style.zIndex = '1999';
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

// 🌈 COLORED LIGHTNING
if (ENV.bands.mid > 0.3) {
  const lightningColor = `hsl(${ENV.bands.mid * 360}, 100%, 80%)`;
  
  const coloredBolt = document.createElement('div');
  coloredBolt.style.position = 'fixed';
  coloredBolt.style.top = '0';
  coloredBolt.style.left = Math.random() * window.innerWidth + 'px';
  coloredBolt.style.width = '4px';
  coloredBolt.style.height = '100%';
  coloredBolt.style.background = `linear-gradient(to bottom, transparent, ${lightningColor}, transparent)`;
  coloredBolt.style.pointerEvents = 'none';
  coloredBolt.style.zIndex = '1998';
  coloredBolt.style.opacity = ENV.bands.mid;
  coloredBolt.style.boxShadow = `0 0 25px ${lightningColor}`;
  document.body.appendChild(coloredBolt);
  
  setTimeout(() => {
    if (document.body.contains(coloredBolt)) {
      document.body.removeChild(coloredBolt);
    }
  }, 300);
}

// ⚡ LIGHTNING STATUS
const status = document.createElement('div');
status.style.position = 'fixed';
status.style.top = '20px';
status.style.left = '20px';
status.style.background = 'rgba(0,0,0,0.8)';
status.style.color = 'white';
status.style.padding = '10px';
status.style.borderRadius = '5px';
status.style.fontFamily = 'monospace';
status.style.zIndex = '3000';
status.style.border = '2px solid #ff6b6b';
document.body.appendChild(status);

status.innerHTML = `
  <div>⚡ LIGHTNING STRIKES ⚡</div>
  <div>🥁 Beat: ${ENV.beat ? 'YES' : 'NO'}</div>
  <div>🔊 Bass: ${(ENV.bands.bass * 100).toFixed(1)}%</div>
  <div>🎶 Mid: ${(ENV.bands.mid * 100).toFixed(1)}%</div>
  <div>⚡ Energy: ${(totalEnergy * 100).toFixed(1)}%</div>
`;

// Return lightning data
return {
  time: new Date().toLocaleTimeString(),
  bpm: Math.round(ENV.bpm),
  beat: ENV.beat,
  bass: Number(ENV.bands.bass.toFixed(3)),
  mid: Number(ENV.bands.mid.toFixed(3)),
  high: Number(ENV.bands.high.toFixed(3)),
  lightning: "⚡ LIGHTNING STRIKES ACTIVE! ⚡",
  energy: Number(totalEnergy.toFixed(3))
};
