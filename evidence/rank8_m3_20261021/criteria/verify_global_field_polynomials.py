#!/usr/bin/env python3
"""Compatibility entry point for the single canonical polynomial verifier.

Default execution is read-only. Pass --write to explicitly regenerate its
receipt in ../noncommutative/general_global_polynomial_validation.json.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'noncommutative'))
from verify_general_global_polynomial import main
if __name__=='__main__': main()
