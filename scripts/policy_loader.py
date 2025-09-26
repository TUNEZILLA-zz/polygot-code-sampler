#!/usr/bin/env python3
"""
Policy loader for PCS performance monitoring
Loads bench/policy.yml and provides typed access to configuration
"""

import yaml
import pathlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parents[1]
POLICY_FILE = ROOT / "bench" / "policy.yml"

@dataclass
class RegressionConfig:
    default_threshold: float
    per_backend: Dict[str, float]
    grace_period_days: int
    min_sample_size: int
    max_regression_ratio: float

@dataclass
class KAnomalyConfig:
    threshold_ratio: float
    min_active_backends: int
    alert_on_consecutive_days: int

@dataclass
class DataQualityConfig:
    outlier_threshold: float
    variance_warning_ratio: float
    min_records_per_day: int
    max_age_days: int

@dataclass
class GovernanceConfig:
    require_approval_threshold: float
    emergency_override_approvers: List[str]
    data_retention_days: int

@dataclass
class RunnerFingerprintingConfig:
    enabled: bool
    track_fields: List[str]
    suppress_alerts_on_runner_change: bool

@dataclass
class WarmupConfig:
    enabled: bool
    warmup_runs: int
    burn_in_runs: int
    record_warmup_times: bool

@dataclass
class DashboardPreset:
    name: str
    filters: Dict[str, Any]

@dataclass
class PolicyConfig:
    version: str
    last_updated: str
    regression: RegressionConfig
    k_anomaly: KAnomalyConfig
    data_quality: DataQualityConfig
    governance: GovernanceConfig
    runner_fingerprinting: RunnerFingerprintingConfig
    warmup: WarmupConfig
    dashboard_presets: List[DashboardPreset]

def load_policy() -> PolicyConfig:
    """Load policy configuration from bench/policy.yml"""
    if not POLICY_FILE.exists():
        raise FileNotFoundError(f"Policy file not found: {POLICY_FILE}")
    
    with open(POLICY_FILE, 'r') as f:
        data = yaml.safe_load(f)
    
    return PolicyConfig(
        version=data['version'],
        last_updated=data['last_updated'],
        regression=RegressionConfig(**data['regression']),
        k_anomaly=KAnomalyConfig(**data['k_anomaly']),
        data_quality=DataQualityConfig(**data['data_quality']),
        governance=GovernanceConfig(**data['governance']),
        runner_fingerprinting=RunnerFingerprintingConfig(**data['runner_fingerprinting']),
        warmup=WarmupConfig(**data['warmup']),
        dashboard_presets=[DashboardPreset(**preset) for preset in data['dashboard_presets']]
    )

def get_regression_threshold(backend: str, policy: PolicyConfig) -> float:
    """Get regression threshold for a specific backend"""
    return policy.regression.per_backend.get(backend, policy.regression.default_threshold)

def get_grace_period(policy: PolicyConfig) -> int:
    """Get grace period in days"""
    return policy.regression.grace_period_days

def get_k_anomaly_threshold(policy: PolicyConfig) -> float:
    """Get K-anomaly detection threshold"""
    return policy.k_anomaly.threshold_ratio

def get_outlier_threshold(policy: PolicyConfig) -> float:
    """Get outlier detection threshold (z-score)"""
    return policy.data_quality.outlier_threshold

def get_variance_warning_ratio(policy: PolicyConfig) -> float:
    """Get variance warning threshold (std/mean ratio)"""
    return policy.data_quality.variance_warning_ratio

def get_approval_required_threshold(policy: PolicyConfig) -> float:
    """Get threshold requiring approval for overrides"""
    return policy.governance.require_approval_threshold

def get_dashboard_presets(policy: PolicyConfig) -> List[DashboardPreset]:
    """Get dashboard preset configurations"""
    return policy.dashboard_presets

if __name__ == "__main__":
    # Test policy loading
    try:
        policy = load_policy()
        print(f"✅ Policy loaded successfully (v{policy.version})")
        print(f"📅 Last updated: {policy.last_updated}")
        print(f"🎯 Regression thresholds: {policy.regression.per_backend}")
        print(f"🔍 K-anomaly threshold: {policy.k_anomaly.threshold_ratio}")
        print(f"📊 Dashboard presets: {len(policy.dashboard_presets)}")
    except Exception as e:
        print(f"❌ Error loading policy: {e}")
        sys.exit(1)

