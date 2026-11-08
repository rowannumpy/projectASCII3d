"""Quick test of ASCII3D engine"""

import sys
sys.path.insert(0, '.')

from engine import ASCIIEngine
from objects import list_objects
from charsets import list_charsets
from looks import list_looks

print("=== ASCII3D Engine Test ===\n")

print("Objects:")
for obj in list_objects():
    print(f"  - {obj}")

print("\nCharsets:")
for cs in list_charsets():
    print(f"  - {cs}")

print("\nLooks:")
for look in list_looks():
    print(f"  - {look}")

print("\n✓ Engine modules load successfully")
print("\nTo run animation:")
print("  python -m ascii3d generate donut")
