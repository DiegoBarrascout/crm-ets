#!/usr/bin/env python3
"""Parse addon XML so CI/Husky fail on malformed QWeb/views."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1] / "addons"
files = list(root.rglob("*.xml"))
if not files:
    print("no XML found under addons/", file=sys.stderr)
    sys.exit(1)
for path in files:
    ET.parse(path)
print(f"ok {len(files)} xml")
