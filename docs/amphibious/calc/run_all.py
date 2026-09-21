import subprocess, sys, pathlib
here = pathlib.Path(__file__).parent
for n in ("mass_amph.py", "hydrostatics_amph.py", "kinematics_amph.py", "architectures_amph.py", "resistance_power_amph.py", "loads_amph.py", "checks_amph.py"):
    print("="*78); print(n); print("="*78)
    subprocess.run([sys.executable, str(here/n)], check=True)
