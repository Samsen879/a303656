#!/usr/bin/env python3
from __future__ import annotations
import sys
from backend_adapter import main
if __name__ == "__main__":
    sys.argv[1:1] = ["--backend", "A"]
    raise SystemExit(main())
