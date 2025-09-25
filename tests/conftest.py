#!/usr/bin/env python3
"""
Pytest configuration for Polyglot Code Sampler golden tests
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import pcs_step3_ts
sys.path.insert(0, str(Path(__file__).parent.parent))

def pytest_addoption(parser):
    """Add custom pytest options"""
    parser.addoption(
        "--update-golden", 
        action="store_true", 
        help="Update golden files instead of comparing"
    )

@pytest.fixture
def update_golden(request):
    """Fixture to check if we should update golden files"""
    return request.config.getoption("--update-golden")

@pytest.fixture
def golden_dir():
    """Fixture to get the golden directory path"""
    return Path(__file__).parent / "golden"
