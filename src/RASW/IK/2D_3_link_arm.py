import math
import numpy as np

l1 = 160
l2 = 160
l3 = 160

offset = math.radians(10)
a1_weight = 1

point_x = 250
point_y = 150


def safe_arccos(x):
    if x > 1.0:
        x = 1.0
    elif x < -1.0:
        x = -1.0
    return np.arccos(x)


def safe_arcsin(x):
    if x > 1.0:
        x = 1.0
    elif x < -1.0:
        x = -1.0
    return np.arcsin(x)


def arm_math(point_x, point_y, offset):
    total_arm_length = l1 + l2 + l3
    distance_to_point = np.sqrt(point_x**2 + point_y**2)
    if distance_to_point > total_arm_length:
        print("Target point is unreachable.")
        return

    # angle1 is base rotation toward the point
    angle1 = a1_weight * np.arctan2(point_y, point_x) + offset

    # Position of joint 2
    p2_x_point = np.cos(angle1) * l1
    p2_y_point = np.sin(angle1) * l1

    # h = distance from joint 2 to target point
    h = np.sqrt((point_x - p2_x_point) ** 2 + (point_y - p2_y_point) ** 2)

    # b = target y, d = joint 2 y
    b = point_y
    d = p2_y_point

    # New angle2 formula with arccos and arcsin parts
    angle2 = -angle1 + (
        safe_arccos((l3**2 - l2**2 - h**2) / (-2 * l2 * h)) + safe_arcsin((b - d) / h)
    )

    # Angle 3 (same as before)
    angle3 = -np.pi + safe_arccos((h**2 - l2**2 - l3**2) / (-2 * l2 * l3))

    print("First angle (rad):", angle1, "→", math.degrees(angle1), "degrees")
    print("Second angle (rad):", angle2, "→", math.degrees(angle2), "degrees")
    print("Third angle (rad):", angle3, "→", math.degrees(angle3), "degrees")


arm_math(point_x, point_y, offset)
