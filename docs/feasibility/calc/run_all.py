"""Run every calc and print the results used in the study."""
import subprocess, sys, pathlib
here = pathlib.Path(__file__).parent
for name in ("mass_budget.py", "mechanism_statics.py", "energy.py", "buoyancy.py", "rollover.py"):
    print("=" * 78); print(name); print("=" * 78)
    subprocess.run([sys.executable, str(here / name)], check=True)
