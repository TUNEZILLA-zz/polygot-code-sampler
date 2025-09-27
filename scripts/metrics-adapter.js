/**
 * Code Live Physics FX - Minimal Metrics Adapter
 * Drop-in metrics adapter with debouncing, clamping, and fallback
 */

class MetricsAdapter {
    constructor(source, options = {}) {
        this.source = source;
        this.debounceMs = options.debounceMs || 100; // 10Hz
        this.timeoutHandle = null;
        this.latest = {
            qps: 0, p95: 30, errorRate: 0, fallbackRatio: 0,
            perBackend: { rust:0.5, ts:0.5, go:0.4, csharp:0.3, sql:0.2, julia:0.2 }
        };
        
        this.startPolling();
    }

    async poll() {
        try {
            const res = await fetch(this.source);
            if (res.ok) {
                const m = await res.json();
                this.latest = this.sanitize(m);
            }
        } catch (error) {
            console.warn('Metrics fetch failed, using fallback:', error);
            this.useFallbackMetrics();
        }
        
        this.timeoutHandle = setTimeout(() => this.poll(), this.debounceMs);
    }

    sanitize(m) {
        const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
        return {
            qps: clamp(m.qps ?? 0, 0, 240),
            p95: clamp(m.p95 ?? 30, 0, 500),
            errorRate: clamp(m.errorRate ?? 0, 0, 1),
            fallbackRatio: clamp(m.fallbackRatio ?? 0, 0, 1),
            perBackend: Object.fromEntries(
                Object.entries(m.perBackend ?? {}).map(([k,v]) => [k, clamp(v, 0, 1)])
            )
        };
    }

    useFallbackMetrics() {
        // Demo generator fallback
        const t = Date.now() * 0.001;
        this.latest = {
            qps: 30 + 20*Math.sin(t*0.02),
            p95: 40 + 30*Math.sin(t*0.017),
            errorRate: Math.max(0, 0.05*Math.sin(t*0.01)),
            fallbackRatio: Math.max(0, 0.08*Math.cos(t*0.012)),
            perBackend: { rust:0.9, ts:0.8, go:0.7, csharp:0.6, sql:0.5, julia:0.4 }
        };
    }

    startPolling() {
        this.poll();
    }

    stopPolling() {
        if (this.timeoutHandle) {
            clearTimeout(this.timeoutHandle);
        }
    }

    getMetrics() {
        return this.latest;
    }
}

export default MetricsAdapter;

