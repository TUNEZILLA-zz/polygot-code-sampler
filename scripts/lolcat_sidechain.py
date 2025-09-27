#!/usr/bin/env python3
"""
LOLcat++ Sidechain Sweet Spots - QPS, error_rate, p95 integration
"""
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string_fx.lolcat_plus import lolcat_plus

class LOLcatSidechain:
    def __init__(self):
        # Sidechain parameters
        self.qps = 0.0
        self.error_rate = 0.0
        self.p95 = 0.0
        
        # Sidechain sweet spots
        self.qps_target = "lolcat_plus.gradient_phase"
        self.qps_slew = 0.8  # cap 0.8/s
        self.qps_ease_in = 250  # ms
        self.qps_ease_out = 200  # ms
        
        self.error_target = "lolcat_plus.chaos"
        self.error_bump = 0.1  # max +0.1
        self.error_fade = 200  # ms decay
        
        self.p95_target_emoji = "lolcat_plus.emoji"
        self.p95_target_trail = "lolcat_plus.trail"
        self.p95_multiplier = 0.75  # ×0.75 when p95 is high
        
        # Current LOLcat++ parameters
        self.emoji = 0.1
        self.chaos = 0.15
        self.trail = 0.2
        self.gradient_phase = 0.0
        self.uwu = 0.3
        self.intensity = 0.5
        
        # Slew limiting
        self.last_qps_time = 0
        self.last_error_time = 0
        self.error_decay_start = 0
        
    def update_metrics(self, qps, error_rate, p95):
        """Update sidechain metrics"""
        self.qps = qps
        self.error_rate = error_rate
        self.p95 = p95
        
    def apply_qps_sidechain(self):
        """Apply QPS sidechain to gradient_phase"""
        current_time = time.time() * 1000  # ms
        
        # Slew limiting for QPS
        if current_time - self.last_qps_time > 16:  # ~60 FPS
            # Ease in/out for smooth transitions
            if self.qps > 0.5:  # High QPS
                # Ease in
                if current_time - self.last_qps_time < self.qps_ease_in:
                    ease_factor = (current_time - self.last_qps_time) / self.qps_ease_in
                else:
                    ease_factor = 1.0
            else:  # Low QPS
                # Ease out
                if current_time - self.last_qps_time < self.qps_ease_out:
                    ease_factor = 1.0 - (current_time - self.last_qps_time) / self.qps_ease_out
                else:
                    ease_factor = 0.0
                    
            # Apply QPS to gradient_phase with slew limiting
            target_phase = min(self.qps * 2.0, 1.0)  # Scale QPS to 0-1
            phase_delta = (target_phase - self.gradient_phase) * ease_factor
            self.gradient_phase += phase_delta * (self.qps_slew / 60.0)  # 60 FPS
            
            # Clamp gradient_phase
            self.gradient_phase = max(0.0, min(1.0, self.gradient_phase))
            self.last_qps_time = current_time
            
    def apply_error_sidechain(self):
        """Apply error_rate sidechain to chaos"""
        current_time = time.time() * 1000  # ms
        
        if self.error_rate > 0.1:  # Error threshold
            # Bump chaos
            chaos_bump = min(self.error_rate * self.error_bump, self.error_bump)
            self.chaos = min(0.5, self.chaos + chaos_bump)
            self.error_decay_start = current_time
        else:
            # Decay chaos back to baseline
            if self.error_decay_start > 0:
                decay_time = current_time - self.error_decay_start
                if decay_time > self.error_fade:
                    # Full decay
                    self.chaos = max(0.15, self.chaos - 0.01)  # Baseline 0.15
                else:
                    # Partial decay
                    decay_factor = decay_time / self.error_fade
                    self.chaos = max(0.15, self.chaos - (chaos_bump * decay_factor))
                    
    def apply_p95_sidechain(self):
        """Apply p95 sidechain to emoji and trail"""
        if self.p95 > 10.0:  # High p95 threshold (ms)
            # Reduce emoji and trail for comfort + performance
            self.emoji *= self.p95_multiplier
            self.trail *= self.p95_multiplier
            
            # Clamp to minimums
            self.emoji = max(0.02, self.emoji)
            self.trail = max(0.05, self.trail)
        else:
            # Restore to normal levels
            self.emoji = min(0.2, self.emoji / self.p95_multiplier)
            self.trail = min(0.6, self.trail / self.p95_multiplier)
            
    def process_sidechain(self):
        """Process all sidechain effects"""
        self.apply_qps_sidechain()
        self.apply_error_sidechain()
        self.apply_p95_sidechain()
        
    def get_lolcat_params(self):
        """Get current LOLcat++ parameters"""
        return {
            "intensity": self.intensity,
            "uwu": self.uwu,
            "chaos": self.chaos,
            "emoji": self.emoji,
            "nyan_trail": self.trail,
            "gradient_phase": self.gradient_phase
        }
        
    def demo_sidechain(self, duration=30):
        """Demo sidechain effects"""
        print("😺 Starting LOLcat++ Sidechain Demo...")
        print("Press Ctrl+C to stop")
        
        try:
            start_time = time.time()
            while time.time() - start_time < duration:
                # Simulate varying metrics
                t = time.time()
                
                # Simulate QPS (0-1)
                qps = 0.3 + 0.4 * (1 + (t * 0.5) % 2) / 2
                
                # Simulate error_rate (0-1)
                error_rate = 0.1 + 0.3 * (1 + (t * 0.3) % 2) / 2
                
                # Simulate p95 (5-15 ms)
                p95 = 5 + 10 * (1 + (t * 0.2) % 2) / 2
                
                # Update metrics
                self.update_metrics(qps, error_rate, p95)
                
                # Process sidechain
                self.process_sidechain()
                
                # Get parameters
                params = self.get_lolcat_params()
                
                # Show status
                print(f"\r😺 QPS: {qps:.2f} | Error: {error_rate:.2f} | P95: {p95:.1f}ms | "
                      f"Phase: {self.gradient_phase:.2f} | Chaos: {self.chaos:.2f} | "
                      f"Emoji: {self.emoji:.2f} | Trail: {self.trail:.2f}", end="")
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n😺 Sidechain demo stopped")
            
    def test_sidechain(self, text="Sidechain test"):
        """Test sidechain with current parameters"""
        params = self.get_lolcat_params()
        result = lolcat_plus(text, **params)
        
        print(f"😺 Sidechain Test Results:")
        print(f"   QPS: {self.qps:.2f} → Gradient Phase: {self.gradient_phase:.2f}")
        print(f"   Error Rate: {self.error_rate:.2f} → Chaos: {self.chaos:.2f}")
        print(f"   P95: {self.p95:.1f}ms → Emoji: {self.emoji:.2f}, Trail: {self.trail:.2f}")
        print(f"   Transformed: {result['text']}")
        print(f"   ANSI: {result['ansi']}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="LOLcat++ Sidechain Sweet Spots")
    parser.add_argument("--demo", action="store_true", help="Run sidechain demo")
    parser.add_argument("--test", action="store_true", help="Test sidechain")
    parser.add_argument("--text", default="Sidechain test", help="Text to transform")
    parser.add_argument("--qps", type=float, default=0.5, help="QPS value")
    parser.add_argument("--error", type=float, default=0.1, help="Error rate")
    parser.add_argument("--p95", type=float, default=8.0, help="P95 latency")
    
    args = parser.parse_args()
    
    sidechain = LOLcatSidechain()
    
    if args.demo:
        sidechain.demo_sidechain()
    elif args.test:
        sidechain.update_metrics(args.qps, args.error, args.p95)
        sidechain.process_sidechain()
        sidechain.test_sidechain(args.text)
    else:
        print("Usage: python3 lolcat_sidechain.py --demo | --test [--qps 0.5 --error 0.1 --p95 8.0]")

if __name__ == "__main__":
    main()
