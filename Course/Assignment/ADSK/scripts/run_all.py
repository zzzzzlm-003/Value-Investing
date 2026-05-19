"""Run all ADSK valuation scripts."""
import subprocess
import os

BASE = os.path.dirname(os.path.abspath(__file__))
for name in ["q5_asset_value", "q6_epv", "q7_growth"]:
    print(f"\n{'='*60}\nRunning {name}.py\n{'='*60}")
    subprocess.run(["python3", os.path.join(BASE, f"{name}.py")], check=True)
