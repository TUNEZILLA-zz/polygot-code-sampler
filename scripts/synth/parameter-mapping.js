/**
 * Code Live - Parameter Mapping for Synth Modulation
 * Maps LFO outputs to physics FX parameters
 */

class ParameterMapper {
    constructor() {
        this.mappings = new Map();
        this.parameterRanges = new Map();
        this.midiCCMappings = new Map();

        // Initialize default parameter ranges
        this.initializeDefaultRanges();
    }

    /**
     * Initialize default parameter ranges for physics FX
     */
    initializeDefaultRanges() {
        // Physics FX parameter ranges
        this.parameterRanges.set('particleCount', { min: 0, max: 1000, default: 100 });
        this.parameterRanges.set('damping', { min: 0, max: 1, default: 0.1 });
        this.parameterRanges.set('turbulence', { min: 0, max: 10, default: 1 });
        this.parameterRanges.set('windStrength', { min: 0, max: 5, default: 0.5 });
        this.parameterRanges.set('gravity', { min: -2, max: 2, default: 0 });
        this.parameterRanges.set('opacity', { min: 0, max: 1, default: 0.8 });
        this.parameterRanges.set('scale', { min: 0.1, max: 3, default: 1 });
        this.parameterRanges.set('rotation', { min: -Math.PI, max: Math.PI, default: 0 });

        // Backend-specific parameters
        this.parameterRanges.set('juliaParallel', { min: 0, max: 1, default: 0.5 });
        this.parameterRanges.set('rustUnsafe', { min: 0, max: 1, default: 0 });
        this.parameterRanges.set('sqlOptimize', { min: 0, max: 1, default: 1 });
        this.parameterRanges.set('goGoroutines', { min: 1, max: 16, default: 4 });
    }

    /**
     * Map LFO output to a physics parameter
     * @param {string} parameter - Parameter name
     * @param {LFO} lfo - LFO instance
     * @param {Object} options - Mapping options
     */
    mapParameter(parameter, lfo, options = {}) {
        const mapping = {
            parameter,
            lfo,
            min: options.min || 0,
            max: options.max || 1,
            offset: options.offset || 0,
            scale: options.scale || 1,
            enabled: options.enabled !== false
        };

        this.mappings.set(parameter, mapping);
    }

    /**
     * Map MIDI CC to a parameter
     * @param {number} cc - MIDI CC number (0-127)
     * @param {string} parameter - Parameter name
     * @param {Object} options - Mapping options
     */
    mapMIDICC(cc, parameter, options = {}) {
        const mapping = {
            cc,
            parameter,
            min: options.min || 0,
            max: options.max || 1,
            offset: options.offset || 0,
            scale: options.scale || 1,
            enabled: options.enabled !== false
        };

        this.midiCCMappings.set(cc, mapping);
    }

    /**
     * Update all mapped parameters
     * @param {number} deltaTime - Time elapsed since last update
     * @returns {Object} Updated parameter values
     */
    updateParameters(deltaTime) {
        const updatedParams = {};

        // Update LFO-mapped parameters
        for (const [parameter, mapping] of this.mappings) {
            if (!mapping.enabled) continue;

            const lfoOutput = mapping.lfo.update(deltaTime);
            const range = this.parameterRanges.get(parameter);

            if (range) {
                // Map LFO output (-1 to 1) to parameter range
                const normalized = (lfoOutput + 1) / 2; // 0 to 1
                const scaled = normalized * (mapping.max - mapping.min) + mapping.min;
                const offset = scaled + mapping.offset;
                const final = offset * mapping.scale;

                // Clamp to parameter range
                updatedParams[parameter] = Math.max(range.min, Math.min(range.max, final));
            }
        }

        return updatedParams;
    }

    /**
     * Handle MIDI CC input
     * @param {number} cc - MIDI CC number
     * @param {number} value - MIDI CC value (0-127)
     * @returns {Object} Updated parameter values
     */
    handleMIDICC(cc, value) {
        const mapping = this.midiCCMappings.get(cc);
        if (!mapping || !mapping.enabled) return {};

        const range = this.parameterRanges.get(mapping.parameter);
        if (!range) return {};

        // Convert MIDI value (0-127) to parameter range
        const normalized = value / 127; // 0 to 1
        const scaled = normalized * (mapping.max - mapping.min) + mapping.min;
        const offset = scaled + mapping.offset;
        const final = offset * mapping.scale;

        // Clamp to parameter range
        const parameterValue = Math.max(range.min, Math.min(range.max, final));

        return { [mapping.parameter]: parameterValue };
    }

    /**
     * Get current parameter values
     * @returns {Object} Current parameter values
     */
    getCurrentParameters() {
        const params = {};

        for (const [parameter, mapping] of this.mappings) {
            if (!mapping.enabled) continue;

            const range = this.parameterRanges.get(parameter);
            if (range) {
                params[parameter] = range.default;
            }
        }

        return params;
    }

    /**
     * Enable/disable parameter mapping
     * @param {string} parameter - Parameter name
     * @param {boolean} enabled - Whether mapping is enabled
     */
    setParameterEnabled(parameter, enabled) {
        const mapping = this.mappings.get(parameter);
        if (mapping) {
            mapping.enabled = enabled;
        }
    }

    /**
     * Remove parameter mapping
     * @param {string} parameter - Parameter name
     */
    removeParameterMapping(parameter) {
        this.mappings.delete(parameter);
    }

    /**
     * Remove MIDI CC mapping
     * @param {number} cc - MIDI CC number
     */
    removeMIDICCMapping(cc) {
        this.midiCCMappings.delete(cc);
    }

    /**
     * Get all active mappings
     * @returns {Object} Active mappings
     */
    getActiveMappings() {
        const active = {
            lfo: [],
            midi: []
        };

        for (const [parameter, mapping] of this.mappings) {
            if (mapping.enabled) {
                active.lfo.push({
                    parameter,
                    lfo: mapping.lfo.getState(),
                    range: { min: mapping.min, max: mapping.max },
                    offset: mapping.offset,
                    scale: mapping.scale
                });
            }
        }

        for (const [cc, mapping] of this.midiCCMappings) {
            if (mapping.enabled) {
                active.midi.push({
                    cc,
                    parameter: mapping.parameter,
                    range: { min: mapping.min, max: mapping.max },
                    offset: mapping.offset,
                    scale: mapping.scale
                });
            }
        }

        return active;
    }

    /**
     * Save mappings to preset
     * @returns {Object} Preset data
     */
    savePreset() {
        return {
            mappings: Array.from(this.mappings.entries()),
            midiMappings: Array.from(this.midiCCMappings.entries()),
            timestamp: Date.now()
        };
    }

    /**
     * Load mappings from preset
     * @param {Object} preset - Preset data
     */
    loadPreset(preset) {
        if (preset.mappings) {
            this.mappings = new Map(preset.mappings);
        }
        if (preset.midiMappings) {
            this.midiCCMappings = new Map(preset.midiMappings);
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ParameterMapper;
} else if (typeof window !== 'undefined') {
    window.ParameterMapper = ParameterMapper;
}
