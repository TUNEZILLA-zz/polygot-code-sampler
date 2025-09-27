/**
 * Code Live - LFO (Low Frequency Oscillator) Module
 * Provides tempo-synced modulation for physics FX parameters
 */

class LFO {
    constructor(options = {}) {
        this.frequency = options.frequency || 1.0; // Hz
        this.amplitude = options.amplitude || 1.0;
        this.phase = options.phase || 0;
        this.waveform = options.waveform || 'sine'; // sine, square, triangle, sawtooth
        this.tempoSync = options.tempoSync || false;
        this.tempo = options.tempo || 120; // BPM
        this.enabled = options.enabled || true;

        this.time = 0;
        this.output = 0;
    }

    /**
     * Update LFO and return current output value
     * @param {number} deltaTime - Time elapsed since last update (seconds)
     * @returns {number} LFO output value (-1 to 1)
     */
    update(deltaTime) {
        if (!this.enabled) return 0;

        this.time += deltaTime;

        // Calculate effective frequency (tempo sync or free-running)
        let effectiveFreq = this.frequency;
        if (this.tempoSync) {
            // Convert BPM to Hz: (BPM / 60) * frequency multiplier
            effectiveFreq = (this.tempo / 60) * this.frequency;
        }

        // Calculate phase
        const phase = (this.time * effectiveFreq * 2 * Math.PI) + this.phase;

        // Generate waveform
        switch (this.waveform) {
            case 'sine':
                this.output = Math.sin(phase);
                break;
            case 'square':
                this.output = Math.sin(phase) > 0 ? 1 : -1;
                break;
            case 'triangle':
                this.output = (2 / Math.PI) * Math.asin(Math.sin(phase));
                break;
            case 'sawtooth':
                this.output = (2 / Math.PI) * Math.atan(Math.tan(phase / 2));
                break;
            default:
                this.output = Math.sin(phase);
        }

        // Apply amplitude
        this.output *= this.amplitude;

        return this.output;
    }

    /**
     * Set tempo for tempo-synced LFOs
     * @param {number} bpm - Beats per minute
     */
    setTempo(bpm) {
        this.tempo = bpm;
    }

    /**
     * Set frequency (Hz or tempo-synced multiplier)
     * @param {number} freq - Frequency in Hz or tempo multiplier
     */
    setFrequency(freq) {
        this.frequency = freq;
    }

    /**
     * Set amplitude (0 to 1)
     * @param {number} amp - Amplitude
     */
    setAmplitude(amp) {
        this.amplitude = Math.max(0, Math.min(1, amp));
    }

    /**
     * Set waveform type
     * @param {string} wave - Waveform type
     */
    setWaveform(wave) {
        const validWaves = ['sine', 'square', 'triangle', 'sawtooth'];
        if (validWaves.includes(wave)) {
            this.waveform = wave;
        }
    }

    /**
     * Enable/disable LFO
     * @param {boolean} enabled - Whether LFO is enabled
     */
    setEnabled(enabled) {
        this.enabled = enabled;
    }

    /**
     * Reset LFO to initial state
     */
    reset() {
        this.time = 0;
        this.output = 0;
    }

    /**
     * Get current output value
     * @returns {number} Current LFO output
     */
    getOutput() {
        return this.output;
    }

    /**
     * Get LFO state for serialization
     * @returns {Object} LFO state
     */
    getState() {
        return {
            frequency: this.frequency,
            amplitude: this.amplitude,
            phase: this.phase,
            waveform: this.waveform,
            tempoSync: this.tempoSync,
            tempo: this.tempo,
            enabled: this.enabled,
            output: this.output
        };
    }

    /**
     * Set LFO state from serialized data
     * @param {Object} state - LFO state
     */
    setState(state) {
        this.frequency = state.frequency || this.frequency;
        this.amplitude = state.amplitude || this.amplitude;
        this.phase = state.phase || this.phase;
        this.waveform = state.waveform || this.waveform;
        this.tempoSync = state.tempoSync !== undefined ? state.tempoSync : this.tempoSync;
        this.tempo = state.tempo || this.tempo;
        this.enabled = state.enabled !== undefined ? state.enabled : this.enabled;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LFO;
} else if (typeof window !== 'undefined') {
    window.LFO = LFO;
}
