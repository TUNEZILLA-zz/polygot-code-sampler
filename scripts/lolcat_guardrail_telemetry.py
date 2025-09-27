#!/usr/bin/env python3
"""
LOLcat++ Guardrail Telemetry Ping - Emit telemetry when clamps engage
"""
import time
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string_fx.lolcat_plus import lolcat_plus

class LOLcatGuardrailTelemetry:
    def __init__(self):
        self.telemetry_events = []
        self.clamp_thresholds = {
            "emoji": 0.2,
            "trail": 0.6,
            "chaos": 0.5,
            "intensity": 1.0
        }
        
    def emit_telemetry(self, reason, parameter, value, threshold, context=None):
        """Emit telemetry event when guardrails engage"""
        event = {
            "timestamp": time.time(),
            "event": "lolcat_guard_trim",
            "reason": reason,
            "parameter": parameter,
            "value": value,
            "threshold": threshold,
            "context": context or {},
            "severity": "warning" if value > threshold * 0.8 else "info"
        }
        
        self.telemetry_events.append(event)
        
        # Print telemetry (in real system, this would go to Grafana)
        print(f"📊 TELEMETRY: {event['event']}{{reason=\"{reason}\", parameter=\"{parameter}\", value={value:.2f}, threshold={threshold:.2f}}}")
        
        return event
        
    def check_guardrails(self, params, context=None):
        """Check parameters against guardrails and emit telemetry if needed"""
        events = []
        
        for param, threshold in self.clamp_thresholds.items():
            if param in params:
                value = params[param]
                if value > threshold:
                    reason = f"{param}_exceeded"
                    event = self.emit_telemetry(reason, param, value, threshold, context)
                    events.append(event)
                    
        return events
        
    def simulate_guardrail_scenarios(self):
        """Simulate various guardrail scenarios"""
        print("😺 LOLcat++ Guardrail Telemetry Demo")
        print("=" * 50)
        
        scenarios = [
            {
                "name": "Normal Operation",
                "params": {"emoji": 0.1, "trail": 0.3, "chaos": 0.2, "intensity": 0.6},
                "context": {"scene": "classic", "metrics_link": 0.5}
            },
            {
                "name": "High Emoji Density",
                "params": {"emoji": 0.25, "trail": 0.3, "chaos": 0.2, "intensity": 0.6},
                "context": {"scene": "stage-punch", "metrics_link": 0.8}
            },
            {
                "name": "Excessive Trail",
                "params": {"emoji": 0.1, "trail": 0.7, "chaos": 0.2, "intensity": 0.6},
                "context": {"scene": "cat-walk", "metrics_link": 0.3}
            },
            {
                "name": "Chaos Overload",
                "params": {"emoji": 0.1, "trail": 0.3, "chaos": 0.6, "intensity": 0.6},
                "context": {"scene": "impact", "metrics_link": 0.9}
            },
            {
                "name": "Multiple Violations",
                "params": {"emoji": 0.25, "trail": 0.7, "chaos": 0.6, "intensity": 0.6},
                "context": {"scene": "data-storm", "metrics_link": 0.95}
            }
        ]
        
        for scenario in scenarios:
            print(f"\n🎭 Scenario: {scenario['name']}")
            print(f"   Params: {scenario['params']}")
            
            events = self.check_guardrails(scenario['params'], scenario['context'])
            
            if events:
                print(f"   ⚠️  {len(events)} guardrail violations detected")
            else:
                print("   ✅ All parameters within safe limits")
                
    def test_motion_watchdog(self):
        """Test motion watchdog telemetry"""
        print("😺 Testing Motion Watchdog Telemetry...")
        print("=" * 50)
        
        # Simulate motion watchdog scenarios
        scenarios = [
            {"reduced_motion": True, "trail": 0.0, "emoji": 0.03, "chaos": 0.05},
            {"reduced_motion": False, "trail": 0.4, "emoji": 0.15, "chaos": 0.3}
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{i}. Motion Watchdog Scenario:")
            print(f"   Reduced Motion: {scenario['reduced_motion']}")
            print(f"   Trail: {scenario['trail']}, Emoji: {scenario['emoji']}, Chaos: {scenario['chaos']}")
            
            # Check if motion watchdog would engage
            if scenario['reduced_motion']:
                if scenario['trail'] > 0.1 or scenario['emoji'] > 0.05 or scenario['chaos'] > 0.1:
                    self.emit_telemetry("motion_watchdog", "reduced_motion", 1.0, 0.0, scenario)
                else:
                    print("   ✅ Motion watchdog satisfied")
            else:
                print("   ℹ️  Motion watchdog not active")
                
    def generate_grafana_metrics(self):
        """Generate Grafana-compatible metrics"""
        print("😺 Generating Grafana Metrics...")
        print("=" * 50)
        
        # Simulate some telemetry events
        self.emit_telemetry("emoji_exceeded", "emoji", 0.25, 0.2, {"scene": "stage-punch"})
        self.emit_telemetry("trail_exceeded", "trail", 0.7, 0.6, {"scene": "cat-walk"})
        self.emit_telemetry("motion_watchdog", "reduced_motion", 1.0, 0.0, {"scene": "studio-safe"})
        
        # Generate metrics summary
        total_events = len(self.telemetry_events)
        warning_events = len([e for e in self.telemetry_events if e['severity'] == 'warning'])
        
        print(f"📊 Total Events: {total_events}")
        print(f"📊 Warning Events: {warning_events}")
        print(f"📊 Info Events: {total_events - warning_events}")
        
        # Group by reason
        reasons = {}
        for event in self.telemetry_events:
            reason = event['reason']
            reasons[reason] = reasons.get(reason, 0) + 1
            
        print("\n📊 Events by Reason:")
        for reason, count in reasons.items():
            print(f"   {reason}: {count}")
            
    def export_telemetry_log(self, filename="lolcat_telemetry.json"):
        """Export telemetry events to JSON log"""
        with open(filename, 'w') as f:
            json.dump(self.telemetry_events, f, indent=2)
            
        print(f"😺 Telemetry log exported to: {filename}")
        print(f"   Events: {len(self.telemetry_events)}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="LOLcat++ Guardrail Telemetry")
    parser.add_argument("--demo", action="store_true", help="Demo guardrail scenarios")
    parser.add_argument("--motion", action="store_true", help="Test motion watchdog")
    parser.add_argument("--grafana", action="store_true", help="Generate Grafana metrics")
    parser.add_argument("--export", action="store_true", help="Export telemetry log")
    parser.add_argument("--emoji", type=float, default=0.1, help="Emoji value to test")
    parser.add_argument("--trail", type=float, default=0.3, help="Trail value to test")
    parser.add_argument("--chaos", type=float, default=0.2, help="Chaos value to test")
    
    args = parser.parse_args()
    
    telemetry = LOLcatGuardrailTelemetry()
    
    if args.demo:
        telemetry.simulate_guardrail_scenarios()
    elif args.motion:
        telemetry.test_motion_watchdog()
    elif args.grafana:
        telemetry.generate_grafana_metrics()
    elif args.export:
        telemetry.simulate_guardrail_scenarios()
        telemetry.export_telemetry_log()
    else:
        # Test specific parameters
        params = {
            "emoji": args.emoji,
            "trail": args.trail,
            "chaos": args.chaos,
            "intensity": 0.6
        }
        
        events = telemetry.check_guardrails(params)
        if events:
            print(f"⚠️  {len(events)} guardrail violations detected")
        else:
            print("✅ All parameters within safe limits")

if __name__ == "__main__":
    main()
