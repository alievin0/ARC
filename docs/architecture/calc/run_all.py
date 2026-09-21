import subprocess, sys, pathlib
here = pathlib.Path(__file__).parent
for n in ("mass_budget_v0.py", "kinematics.py", "steering.py", "ski_track.py", "energy_buoyancy_v0.py"):
    print("="*78); print(n); print("="*78)
    subprocess.run([sys.executable, str(here/n)], check=True)
