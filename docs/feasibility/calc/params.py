"""Reference Configuration RC-0 for the ARC-2B feasibility study.

EVERY value in this file is an ASSUMPTION or a DERIVED value. None is a
specification. Each carries a tag:

  ASSUMPTION  - chosen for the study, with the justification in the comment
  BENCHMARK   - taken from a cited real product (see docs/feasibility/REFERENCES.md)
  DERIVED     - computed by one of the calc scripts from the above

The purpose of RC-0 is to make the arithmetic in the study reproducible, not
to define the vehicle. Change a value here and re-run `python3 run_all.py`.
"""

G = 9.81  # m/s^2

# ---------------------------------------------------------------------------
# Envelope (ASSUMPTION: sized like a full-size sport-utility ATV so that the
# rider position, tyre sizes and trailer interfaces are conventional).
# Benchmarks: Polaris Sportsman 570 / Can-Am Outlander 700 class -- see
# REFERENCES.md, entries [ATV-1]..[ATV-3].
# ---------------------------------------------------------------------------
WHEELBASE_M = 1.30          # ASSUMPTION (benchmarks 1.27-1.30 m)
TRACK_M = 0.98              # ASSUMPTION tyre-centre track, road mode (benchmarks ~0.95-1.0 m)
OVERALL_LENGTH_M = 2.10     # ASSUMPTION (benchmarks 2.1-2.2 m)
OVERALL_WIDTH_M = 1.22      # ASSUMPTION (benchmarks 1.2-1.25 m)
GROUND_CLEARANCE_ROAD_M = 0.28   # ASSUMPTION (benchmarks 0.28-0.30 m)
GROUND_CLEARANCE_HIGH_M = 0.48   # ASSUMPTION robotic-mode target (+0.20 m)
TYRE_OD_M = 0.66            # ASSUMPTION 26 in class tyre (26x8-12 / 26x10-12)
TYRE_WIDTH_M = 0.25
SEAT_HEIGHT_M = 0.88        # ASSUMPTION (benchmarks 0.85-0.90 m)

# ---------------------------------------------------------------------------
# Mass budget (bottom-up ASSUMPTIONS; see mass_budget.py for the build-up)
# ---------------------------------------------------------------------------
RIDER_MASS_KG = 100.0       # ASSUMPTION 95th-percentile male + gear
CARGO_MASS_KG = 50.0        # ASSUMPTION rear rack / hitch tongue allowance
PAYLOAD_KG = RIDER_MASS_KG + CARGO_MASS_KG

# ---------------------------------------------------------------------------
# Corner module geometry (ASSUMPTION; used by mechanism_statics.py)
# ---------------------------------------------------------------------------
ARM_LENGTH_M = 0.45         # pivot axis to wheel centre, trailing/leading arm
ARM_ANGLE_ROAD_DEG = 15.0   # arm below horizontal at road ride height (static)
ARM_ANGLE_HIGH_DEG = 45.0   # arm angle at maximum clearance
ARM_ANGLE_RETRACT_DEG = -110.0  # arm swung up and over into the bay
WHEEL_TRAVEL_ROAD_M = 0.22  # ASSUMPTION (benchmarks 0.21-0.25 m)
SPRING_MOTION_RATIO = 0.55  # ASSUMPTION spring travel / wheel travel (typical 0.5-0.7)
ACTUATOR_LEVER_M = 0.16     # ASSUMPTION lever from carrier pivot to actuator rod end

# Dynamic load factors (ASSUMPTION, conventional off-road chassis practice;
# see Part 10 for provenance of each factor)
LOAD_FACTOR_BUMP = 3.0
LOAD_FACTOR_LANDING = 5.0
LOAD_FACTOR_LATERAL = 1.5
LOAD_FACTOR_BRAKING = 1.2

# ---------------------------------------------------------------------------
# Energy / propulsion (ASSUMPTION, see energy.py)
# ---------------------------------------------------------------------------
ROAD_SPEED_MAX_KPH = 60.0
C_RR_GRAVEL = 0.04          # ASSUMPTION rolling resistance on packed dirt/gravel
C_RR_SNOW_TRACK = 0.12      # ASSUMPTION track internal + snow resistance
CDA_M2 = 1.10               # ASSUMPTION rider upright on an ATV
AIR_DENSITY = 1.20
DRIVE_EFFICIENCY = 0.85     # battery to wheel, incl. inverter, motor, gears
PACK_ENERGY_DENSITY_WH_KG = 150.0  # ASSUMPTION pack-level (see Part 11)
USABLE_SOC_FRACTION = 0.85

# ---------------------------------------------------------------------------
# Marine (ASSUMPTION, see buoyancy.py)
# ---------------------------------------------------------------------------
WATER_DENSITY = 1000.0      # fresh water (worst case for buoyancy)
HULL_LENGTH_M = 1.95        # hull tub length within the ATV envelope
HULL_BEAM_M = 1.10          # hull tub beam between wheel bays
HULL_DEPTH_M = 0.45         # hull depth from keel to deck edge
HULL_BLOCK_COEFF = 0.62     # ASSUMPTION for a shallow-V tub with bays removed
WHEEL_BAY_VOLUME_M3 = 4 * (0.70 * 0.32 * 0.40)  # four bays subtracted from tub
