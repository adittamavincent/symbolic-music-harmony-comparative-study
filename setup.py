#!/usr/bin/env python3
"""
setup.py — Backward compatibility wrapper.
Delegates to scripts/bootstrap_models.py to initialize models and dependencies.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from bootstrap_models import main

if __name__ == "__main__":
    main()

