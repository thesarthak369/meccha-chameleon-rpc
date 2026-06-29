"""
Build script — converts the PNG icon to .ico and packages rpc.py into an .exe
Run once:  python build.py
"""

import subprocess
import sys
from pathlib import Path

SRC_PNG = Path(r"C:\Users\sarth\.gemini\antigravity\brain\f62b45cd-fe63-499c-953c-881c044eb324\meccha_icon_1782738878646.png")
ICO_OUT = Path(r"E:\C folder\Documents\Code\Discord RPC\meccha_icon.ico")

# ── Step 1: Convert PNG → ICO ────────────────────────────────
print("Converting icon PNG -> ICO...")
try:
    from PIL import Image
    img = Image.open(SRC_PNG).convert("RGBA")
    # Generate multiple sizes for a proper .ico file
    sizes = [(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)]
    icons = [img.resize(s, Image.LANCZOS) for s in sizes]
    icons[0].save(
        ICO_OUT,
        format="ICO",
        sizes=sizes,
        append_images=icons[1:],
    )
    print(f"  Icon saved -> {ICO_OUT}")
except Exception as e:
    print(f"  ERROR converting icon: {e}")
    sys.exit(1)

# ── Step 2: Build exe with PyInstaller ──────────────────────
print("\nBuilding exe with PyInstaller...")
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",                     # Single .exe file
    "--console",                     # Keep console window (so you see status)
    f"--icon={str(ICO_OUT)}",             # Custom chameleon icon
    "--name=MECCHA CHAMELEON RPC",   # Exe name
    "--distpath=.",                  # Output to current folder
    "--workpath=build_tmp",          # Temp files go here
    "--specpath=build_tmp",          # Spec file goes here
    "rpc.py",
]

result = subprocess.run(cmd)

if result.returncode == 0:
    print("\n" + "="*50)
    print("  SUCCESS!")
    print("  Your exe is ready: 'MECCHA CHAMELEON RPC.exe'")
    print("="*50)
else:
    print("\nBuild failed. Check output above.")
    sys.exit(1)
