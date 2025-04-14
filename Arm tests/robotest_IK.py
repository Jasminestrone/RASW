import matplotlib.pyplot as plt
import numpy as np
import math
import seaborn as sns
import matplotlib.animation as animation

sns.set_theme(style="darkgrid")

# Arm parameters
l1 = 160
l2 = 160
l3 = 160

offset = math.radians(10)
a1_weight = 1

point_x = 400
point_y = 200


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


# Define the rest position (arm straight along x-axis)
rest_angles = [0, 0, 0]
joint_lengths = [l1, l2, l3]

# Compute target joint angles
target_angles = arm_math(point_x, point_y, offset)
if target_angles is None:
    print("Cannot reach target point. Exiting.")
    exit()

# Set up the animation
fig, ax = plt.subplots(figsize=(10, 6))
ax.xaxis.set_tick_params(labelsize=10)
ax.yaxis.set_tick_params(labelsize=10)
(line,) = ax.plot([], [], "o-", linewidth=3, markersize=8, color="blue", label="Arm")
(target_point,) = ax.plot([], [], "rx", markersize=10, label="Target")
target_label = ax.text(
    point_x + 10, point_y + 10, "(400, 200)", color="red", fontsize=12, visible=True
)

ax.set_xlim(0, 500)
ax.set_ylim(0, 500)
ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")
ax.set_title("3-Joint Arm Moving from Rest to Target")
ax.legend(fontsize=12)
ax.set_aspect("equal", adjustable="box")

# More grid lines
tick_spacing = 50
ax.set_xticks(np.arange(0, 501, tick_spacing))
ax.set_yticks(np.arange(0, 501, tick_spacing))
ax.minorticks_on()
ax.grid(which="major", color="gray", linewidth=0.8)
ax.grid(which="minor", color="lightgray", linestyle=":", linewidth=0.5)

# Number of frames for the animation
frames = 50


def interpolate_angles(start_angles, end_angles, t):
    """Interpolate between start and end angles at position t (0 to 1)"""
    return [start + t * (end - start) for start, end in zip(start_angles, end_angles)]


def init():
    line.set_data([], [])
    target_point.set_data([], [])
    target_point.set_visible(True)
    target_label.set_visible(True)
    return line, target_point, target_label


def animate(i):
    t = i / frames if i < frames else 1.0
    current_angles = interpolate_angles(rest_angles, target_angles, t)
    positions = forward_kinematics(current_angles, joint_lengths)
    x_vals, y_vals = zip(*positions)

    line.set_data(x_vals, y_vals)

    if t > 0.5:
        target_point.set_data([point_x], [point_y])
        target_point.set_visible(True)
        target_label.set_visible(True)
    else:
        target_point.set_data([], [])
        target_point.set_visible(True)
        target_label.set_visible(True)

    return line, target_point, target_label


# Create the animation
ani = animation.FuncAnimation(
    fig, animate, frames=frames + 10, init_func=init, blit=True, interval=50
)

plt.tight_layout()
plt.show()
