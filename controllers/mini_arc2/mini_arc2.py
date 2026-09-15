"""MINI ARC-2 -- keyboard tele-operation controller (v0.1).

Drives the four wheel motors of the MiniARC2 robot defined in
``worlds/mini_arc2.wbt``.

Keys (click inside the 3D view first so it has keyboard focus):

    W       drive forward
    S       drive in reverse
    A       turn left
    D       turn right
    SPACE   stop

This is intentionally the simplest thing that works: no autonomy, no AI, no
state machine. Skid steering -- the two left wheels share one speed and the
two right wheels share another.
"""

from controller import Keyboard, Robot

# --- tuning knobs -----------------------------------------------------------
# Wheel speeds are in radians per second. The wheel radius is 0.0325 m, so
# 6.0 rad/s is about 0.20 m/s on the ground.
DRIVE_SPEED = 6.0    # forward / reverse
TURN_SPEED = 4.0     # each side, in opposite directions, for a spin turn

# Device names. These must match the names used in mini_arc2.wbt.
LEFT_MOTORS = ["front_left_wheel_motor", "rear_left_wheel_motor"]
RIGHT_MOTORS = ["front_right_wheel_motor", "rear_right_wheel_motor"]
CAMERA_NAME = "camera"
DISTANCE_SENSOR_NAME = "front_distance_sensor"

# How often to print a sensor line, in simulation steps.
STATUS_EVERY = 32


def make_wheel_motor(robot, name):
    """Fetch a motor and put it in velocity mode (infinite position target)."""
    motor = robot.getDevice(name)
    motor.setPosition(float("inf"))
    motor.setVelocity(0.0)
    return motor


def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    left_motors = [make_wheel_motor(robot, n) for n in LEFT_MOTORS]
    right_motors = [make_wheel_motor(robot, n) for n in RIGHT_MOTORS]

    camera = robot.getDevice(CAMERA_NAME)
    camera.enable(timestep)

    distance_sensor = robot.getDevice(DISTANCE_SENSOR_NAME)
    distance_sensor.enable(timestep)

    keyboard = robot.getKeyboard()
    keyboard.enable(timestep)

    print("=" * 58)
    print("MINI ARC-2 ready.")
    print("  W = forward   S = reverse   A = left   D = right   SPACE = stop")
    print("  Click inside the 3D view first, or the keys go to the menus.")
    print("  camera %dx%d | distance sensor '%s'"
          % (camera.getWidth(), camera.getHeight(), DISTANCE_SENSOR_NAME))
    print("=" * 58)

    command = "STOP"
    step_count = 0

    while robot.step(timestep) != -1:
        step_count += 1

        # Read every key currently held down. getKey() returns -1 when there
        # is nothing left to report this step.
        keys = []
        key = keyboard.getKey()
        while key != -1:
            keys.append(key)
            key = keyboard.getKey()

        left_speed = 0.0
        right_speed = 0.0
        new_command = "STOP"

        for key in keys:
            # Webots ORs modifier flags (SHIFT/CTRL/ALT) into the high bits of
            # the key code. Keyboard.KEY masks them off and leaves the key
            # itself, so holding SHIFT does not break the controls.
            key = key & Keyboard.KEY
            letter = chr(key)
            if letter in ("W", "w"):
                left_speed, right_speed = DRIVE_SPEED, DRIVE_SPEED
                new_command = "FORWARD"
            elif letter in ("S", "s"):
                left_speed, right_speed = -DRIVE_SPEED, -DRIVE_SPEED
                new_command = "REVERSE"
            elif letter in ("A", "a"):
                left_speed, right_speed = -TURN_SPEED, TURN_SPEED
                new_command = "TURN LEFT"
            elif letter in ("D", "d"):
                left_speed, right_speed = TURN_SPEED, -TURN_SPEED
                new_command = "TURN RIGHT"
            elif key == ord(" "):
                left_speed, right_speed = 0.0, 0.0
                new_command = "STOP"
                break

        for motor in left_motors:
            motor.setVelocity(left_speed)
        for motor in right_motors:
            motor.setVelocity(right_speed)

        if new_command != command:
            command = new_command
            print("[%7.2f s] %-10s  left %+5.1f rad/s  right %+5.1f rad/s"
                  % (robot.getTime(), command, left_speed, right_speed))

        if step_count % STATUS_EVERY == 0:
            # The lookup table in the world file returns millimetres, and
            # saturates at 1000 mm when nothing is within range.
            millimetres = distance_sensor.getValue()
            if millimetres >= 999.0:
                reading = "clear"
            else:
                reading = "%.0f mm ahead" % millimetres
            print("[%7.2f s] %-10s  distance: %s"
                  % (robot.getTime(), command, reading))


if __name__ == "__main__":
    main()
