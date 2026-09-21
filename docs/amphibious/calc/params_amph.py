"""ARC-2B amphibious study parameters. Tags: TARGET / TBD / DERIVED / BENCH.
Body frame as in docs/architecture: origin on the ground under the wheelbase
midpoint (ROAD static), +X forward, +Y left, +Z up. Fresh water (1000 kg/m^3)
is used throughout as the conservative case (seawater gives ~2.5% more lift)."""
import math
G = 9.81
RHO = 1000.0

# --- Land vehicle (from docs/architecture) ---------------------------------
CURB_LAND = 487.0
RIDER = 100.0
CARGO_WATER = 25.0          # TARGET: cargo allowance afloat (land cargo is 50 kg)
CG_Z_LAND_RIDER = 0.60      # TARGET (with rider), see architecture
WHEELBASE = 1.30
TRACK = 0.98
TYRE_R = 0.33
TYRE_W = 0.25
TYRE_Y_IN, TYRE_Y_OUT = 0.365, 0.615
L_ARM = 0.50
PIV_Z = 0.434
PIV_X_F, PIV_X_R = 0.161, -0.161
FENDER_CROWN_Z = 0.83
FENDER_TOP_Y = (0.36, 0.62)
FENDER_SIDE_Z = (0.62, 0.84)   # the side band that becomes the rail
OVERALL_W_LAND = 1.24
GROUND_CLEARANCE = 0.28
MAX_STEER_OUTER = 32.0

# --- Watertight tub (design change to the lower body) ------------------------
TUB_X = (-0.85, 0.85)      # TARGET length 1.70 m
TUB_LOWER_Y, TUB_LOWER_Z = 0.30, (0.28, 0.41)   # between the sill outer faces
TUB_UPPER_Y, TUB_UPPER_Z = 0.36, (0.41, 0.85)   # inner arch walls up to the rim
TUB_CB = 0.90              # TARGET block coefficient for a box tub with rounded ends
TUB_RIM_Z = 0.85

# --- Fold-down rail + inflatable tube (Architecture A2, selected) -----------
RAIL_HINGE = (0.62, 0.62)  # (Y, Z) hinge line along the fender lower edge
RAIL_LENGTH = 0.22         # panel height = deployed cantilever
RAIL_FLANGE = 0.15         # top return = deployed down-flange (0.15 m: puts the tube lower than the rail deck)
TUBE_D = 0.50              # TARGET
TUBE_L = 2.40              # overall incl. cones
TUBE_L_EFF = 2.20          # DERIVED-approx: cylindrical equivalent length for volume
TUBE_Y = RAIL_HINGE[0] + RAIL_LENGTH + TUBE_D/2      # 1.09
TUBE_Z = RAIL_HINGE[1] - 0.10                       # two bolt-rope tracks on the flange (Z 0.60 and 0.49) hold the tube centre ~0.10 m below the rail deck
TUBE_P_BAR = 0.20          # BENCH-range for RIB-type tubes (unsourced here, verify)
TUBE_CHAMBERS = 3
TUBE_STORED_VOL = 0.006    # m^3 per tube rolled (4.2 m^2 x ~1.4 mm)

# --- Stern pod ---------------------------------------------------------------
POD_P_KW = 8.0             # TARGET shaft power, sized by resistance_power_amph.py
POD_DUCT_D = 0.30
POD_ARM_L = 0.50
POD_HINGE = (-0.75, 0.32)  # (X, Z) transverse hinge on the rear cross-member, under the rack
POD_STOW_ANGLE = 45.0      # deg above horizontal, arm pointing aft (stowed)
POD_DEPLOY_ANGLE = -20.0   # deg below horizontal, arm pointing aft (deployed)
POD_STEER = 35.0           # deg vectoring

# --- Wheel states used afloat ---------------------------------------------------
TH_WATER = -2.0            # carrier angle afloat (existing hard stop)
TH_HIGH = 38.0
TH_LIFT = 50.0
TH_ROAD = 12.0

# --- Swamped-flotation foam (closed-cell PE/PU in the fender cavities, above the arches)
FOAM_Y = (0.36, 0.62)
FOAM_Z = (0.64, 0.83)
FOAM_X = (-0.95, 0.95)
FOAM_FILL = 0.85           # fraction of the cavity filled (tube roll and blower occupy the rest)
RACK_TIP_X_AMPH = -1.28    # TARGET: the amphibious variant rack is 0.18 m longer to cover the stowed pod (30 mm margin)
