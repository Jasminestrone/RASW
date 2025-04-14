import matplotlib.pyplot as plt
import numpy as np
import math
import seaborn as sns

sns.set_theme(style="darkgrid")

# Arm parameters
l1 = 160
l2 = 160
l3 = 160

offset = math.radians(10)
a1_weight = 1

point_x = 250
point_y = 150


def safe_arccos(x):
    return np.arccos(np.clip(x, -1.0, 1.0))


def safe_arcsin(x):
    return np.arcsin(np.clip(x, -1.0, 1.0))


def arm_math(point_x, point_y, offset):
    total_arm_length = l1 + l2 + l3
    distance_to_point = np.sqrt(point_x**2 + point_y**2)
    if distance_to_point > total_arm_length:
        print("Target point is unreachable.")
        return None

    angle1 = a1_weight * np.arctan2(point_y, point_x) + offset

    p2_x = np.cos(angle1) * l1
    p2_y = np.sin(angle1) * l1

    h = np.sqrt((point_x - p2_x) ** 2 + (point_y - p2_y) ** 2)

    b = point_y
    d = p2_y

    angle2 = -angle1 + (
        safe_arccos((l3**2 - l2**2 - h**2) / (-2 * l2 * h)) + safe_arcsin((b - d) / h)
    )

    angle3 = -np.pi + safe_arccos((h**2 - l2**2 - l3**2) / (-2 * l2 * l3))

    return angle1, angle2, angle3


def forward_kinematics(joint_angles, joint_lengths):
    x, y = 0, 0
    cumulative_angle = 0
    positions = [(x, y)]

    for angle, length in zip(joint_angles, joint_lengths):
        cumulative_angle += angle
        x += length * np.cos(cumulative_angle)
        y += length * np.sin(cumulative_angle)
        positions.append((x, y))

    return positions


# Compute joint angles
angles = arm_math(point_x, point_y, offset)
if angles:
    joint_lengths = [l1, l2, l3]
    positions = forward_kinematics(angles, joint_lengths)

    # Extract x and y for plotting
    x_vals, y_vals = zip(*positions)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, "o-", linewidth=3, markersize=8, color="blue", label="Arm")
    plt.plot(point_x, point_y, "rx", markersize=10, label="Target")
    plt.xlim(-500, 500)
    plt.ylim(-500, 500)
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.title("3-Joint Arm Reaching for Target Point")
    plt.legend()
    plt.grid(True)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()
