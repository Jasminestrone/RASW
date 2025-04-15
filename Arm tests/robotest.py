import matplotlib.pyplot as plt
import numpy as np
import math
import seaborn as sns
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec

# Set the visual theme
sns.set_theme(style="darkgrid")

# Common arm parameters
l1 = 160
l2 = 160
l3 = 160
l4 = 160  # Only used for 4-joint arm

# Target point for 3-joint arm
point_x_3 = 400
point_y_3 = 200

# Target point for 4-joint arm (calculated from the joint angles)
a1_deg = 45
a2_deg = -30
a3_deg = 45
a4_deg = -20

# Convert degrees to radians for 4-joint arm
a1 = np.radians(a1_deg)
a2 = np.radians(a2_deg)
a3 = np.radians(a3_deg)
a4 = np.radians(a4_deg)

# 4-joint arm angles and lengths
joint_angles_4 = [a1, a2, a3, a4]
joint_lengths_4 = [l1, l2, l3, l4]


# Calculate the endpoint of the 4-joint arm to use as its target
def calc_endpoint(angles, lengths):
    x, y = 0, 0
    cumulative_angle = 0
    for angle, length in zip(angles, lengths):
        cumulative_angle += angle
        x += length * np.cos(cumulative_angle)
        y += length * np.sin(cumulative_angle)
    return x, y


point_x_4, point_y_4 = calc_endpoint(joint_angles_4, joint_lengths_4)

# 3-joint arm parameters
offset = math.radians(10)
a1_weight = 1
joint_lengths_3 = [l1, l2, l3]


# Helper functions for 3-joint arm
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


# Common forward kinematics function
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


# Compute target joint angles for 3-joint arm
target_angles_3 = arm_math(point_x_3, point_y_3, offset)
if target_angles_3 is None:
    print("Cannot reach target point. Exiting.")
    exit()

# Define the rest positions
rest_angles_3 = [0, 0, 0]
rest_angles_4 = [0, 0, 0, 0]

# Set up the animation with stacked subplots
fig = plt.figure(figsize=(10, 12))
gs = GridSpec(2, 1, figure=fig, height_ratios=[1, 1])
ax1 = fig.add_subplot(gs[0, 0])  # 3-joint arm (top)
ax2 = fig.add_subplot(gs[1, 0])  # 4-joint arm (bottom)

# Configure 3-joint arm plot
(line1,) = ax1.plot(
    [], [], "o-", linewidth=3, markersize=8, color="blue", label="3-Joint Arm"
)
(target_point1,) = ax1.plot([], [], "rx", markersize=10, label="Target")
target_label1 = ax1.text(
    point_x_3 + 10,
    point_y_3 + 10,
    f"({int(point_x_3)}, {int(point_y_3)})",
    color="red",
    fontsize=12,
    visible=False,
)
end_effector_text1 = ax1.text(0, 0, "", color="blue", fontsize=12, visible=False)

# Configure 4-joint arm plot
(line2,) = ax2.plot(
    [], [], "o-", linewidth=3, markersize=8, color="green", label="4-Joint Arm"
)
(target_point2,) = ax2.plot([], [], "rx", markersize=10, label="Target")
target_label2 = ax2.text(
    point_x_4 + 10,
    point_y_4 + 10,
    f"({int(point_x_4)}, {int(point_y_4)})",
    color="red",
    fontsize=12,
    visible=False,
)
end_effector_text2 = ax2.text(0, 0, "", color="green", fontsize=12, visible=False)

# Configure axes with identical settings for better comparison
for ax in [ax1, ax2]:
    ax.set_xlim(0, 701)
    ax.set_ylim(0, 451)
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.set_aspect("equal", adjustable="box")

    # Add grid lines
    tick_spacing = 50
    ax.set_xticks(np.arange(0, 701, tick_spacing))
    ax.set_yticks(np.arange(0, 451, tick_spacing))
    ax.minorticks_on()
    ax.grid(which="major", color="gray", linewidth=0.8)
    ax.grid(which="minor", color="lightgray", linestyle=":", linewidth=0.5)
    ax.legend(fontsize=12, loc="upper left")

ax1.set_title("3-Joint Arm Moving to Target")
ax2.set_title("4-Joint Arm Movement")

# Number of frames for the animation
frames = 60


def interpolate_angles(start_angles, end_angles, t):
    """Interpolate between start and end angles at position t (0 to 1)"""
    return [start + t * (end - start) for start, end in zip(start_angles, end_angles)]


def init():
    line1.set_data([], [])
    target_point1.set_data([], [])
    end_effector_text1.set_text("")

    line2.set_data([], [])
    target_point2.set_data([], [])
    end_effector_text2.set_text("")

    return (
        line1,
        target_point1,
        target_label1,
        end_effector_text1,
        line2,
        target_point2,
        target_label2,
        end_effector_text2,
    )


def animate(i):
    t = i / frames if i < frames else 1.0

    # Update 3-joint arm
    current_angles_3 = interpolate_angles(rest_angles_3, target_angles_3, t)
    positions_3 = forward_kinematics(current_angles_3, joint_lengths_3)
    x_vals_3, y_vals_3 = zip(*positions_3)
    line1.set_data(x_vals_3, y_vals_3)

    # Show target and update end effector position for 3-joint arm
    target_point1.set_data([point_x_3], [point_y_3])
    target_label1.set_visible(True)

    end_x_3, end_y_3 = x_vals_3[-1], y_vals_3[-1]
    end_effector_text1.set_position((end_x_3 + 10, end_y_3 - 20))
    end_effector_text1.set_text(f"End: ({int(end_x_3)}, {int(end_y_3)})")
    end_effector_text1.set_visible(True)

    # Update 4-joint arm
    current_angles_4 = interpolate_angles(rest_angles_4, joint_angles_4, t)
    positions_4 = forward_kinematics(current_angles_4, joint_lengths_4)
    x_vals_4, y_vals_4 = zip(*positions_4)
    line2.set_data(x_vals_4, y_vals_4)

    # Show target and update end effector position for 4-joint arm
    target_point2.set_data([point_x_4], [point_y_4])
    target_label2.set_visible(True)

    end_x_4, end_y_4 = x_vals_4[-1], y_vals_4[-1]
    end_effector_text2.set_position((end_x_4 + 10, end_y_4 - 20))
    end_effector_text2.set_text(f"End: ({int(end_x_4)}, {int(end_y_4)})")
    end_effector_text2.set_visible(True)

    return (
        line1,
        target_point1,
        target_label1,
        end_effector_text1,
        line2,
        target_point2,
        target_label2,
        end_effector_text2,
    )


# Create the animation
ani = animation.FuncAnimation(
    fig, animate, frames=frames + 10, init_func=init, blit=True, interval=50
)

# Set up figure for better viewing
plt.tight_layout()

# Save the animation as a GIF file
gif_filename = "arm_animation.gif"
print(f"Saving animation to {gif_filename}...")
ani.save(gif_filename, writer="pillow", fps=20, dpi=100)
print(f"Animation saved as {gif_filename}")

# Display the animation in the notebook/interactive environment
plt.show()
