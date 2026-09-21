"""ARC-2B V0 master parameters.

STATUS TAGS (every value carries one):
  TARGET  - design target chosen in this document, to be validated
  TBD     - placeholder to be replaced by measurement or supplier data
  DERIVED - computed by a script in this folder from the above
  BENCH   - benchmark from a cited source (see docs/feasibility/REFERENCES.md)

Coordinate system (vehicle body frame, used in every drawing of the CAD package):
  origin  : on the ground plane, on the centreline, at the wheelbase midpoint,
            with the vehicle in ROAD mode at static ride height
  +X      : forward      +Y : left      +Z : up

Differences from the feasibility study's RC-0 (docs/feasibility/calc/params.py):
  * front arm is LEADING (pivot behind the wheel), rear arm TRAILING; both 0.50 m
  * carrier angles 12 / 38 / 50 deg (road / high / lift) instead of 15 / 45 / 60
  * brakes are inboard on the carrier (anti-dive reason, see kinematics.py)
  * mass budget refined upward (485 kg curb) after adding protection, seat,
    fluids and a heavier corner module
"""
import math
G = 9.81

# --- Master geometry (TARGET unless noted) ----------------------------------
WHEELBASE = 1.30
TRACK_F = 0.98
TRACK_R = 0.98
OVERALL_L = 2.15          # nose to rack tip
OVERALL_W = 1.24          # fender to fender (tyre outer faces at +-0.615 -> W >= 1.23)
OVERALL_H = 1.16          # ground to handlebar grips, road mode, TBD by ergonomics
GROUND_CLEARANCE_ROAD = 0.28
TYRE_OD = 0.66            # 26 in class
TYRE_W = 0.25             # 10 in class tyre section  (26x10-12)
WHEEL_DIA_IN = 12
WHEEL_R = TYRE_OD / 2     # 0.33 m loaded radius approximated as free radius (TBD)
SEAT_H = 0.88             # TARGET, benchmarks 0.85-0.90 m
SEAT_X = -0.10            # seat reference point (rider hip) X
FOOTBOARD_Z = 0.42        # top surface, road mode
FOOTBOARD_X = (-0.25, 0.23)   # DERIVED constraint from the front-wheel sweep (kinematics.py)
FOOTBOARD_Y = (0.18, 0.36)
BAR_GRIP = (0.28, 0.36, 1.16) # X, +-Y, Z of handlebar grips, TBD

# --- Corner module kinematics ------------------------------------------------
L_ARM = 0.50              # pivot axis to wheel centre
TH_ROAD = 12.0            # arm angle below horizontal at static ride height
TH_HIGH = 38.0            # robotic 'high' (+0.20 m)
TH_LIFT = 50.0            # single-corner self-lift / maximum
TH_RETRACT = -50.0        # marine variant only: wheel above the pivot
BUMP = 0.12               # wheel travel above ride height
DROOP = 0.10              # wheel travel below ride height
WHEEL_OFFSET_Y = 0.15     # wheel centre plane outboard of the arm centreline
ARM_PLANE_Y = TRACK_F/2 - WHEEL_OFFSET_Y   # 0.34
PIVOT_BEARING_SPACING = 0.15
MOTION_RATIO = 0.55       # spring travel / wheel travel, TARGET
ACT_LEVER = 0.16          # carrier lever radius for the linear actuator
ACT_ANGLE_OFFSET_MAX = 25.0   # max deviation of the actuator line from perpendicular over the sweep

# --- Brakes / steering ------------------------------------------------------
BRAKE_FRONT_FRACTION = 0.65
DRIVE_REAR_FRACTION = 0.60
MAX_STEER_OUTER = 32.0    # deg
MAX_STEER_INNER = 42.0
KNUCKLE_ARM = 0.12        # steering arm length
KPI = 8.0
CASTER = 5.0

# --- Mass / loads (see mass_budget_v0.py) ----------------------------------
RIDER = 100.0
CARGO = 50.0

# --- Loads factors (TARGET, replace by drop tests) ---------------------------
LF_BUMP = 3.0
LF_LANDING = 5.0
LF_LATERAL = 1.5
LF_BRAKE = 1.2
