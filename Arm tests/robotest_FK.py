import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

# Set the visual theme
sns.set_theme(style="darkgrid")

# ----------------------
# Arm Configuration
# ----------------------

# Define lengths of the 4 arm segments
l1 = 160
l2 = 160
l3 = 160
l4 = 160

# Define joint angles in degrees (you can tweak these)
a1_deg = 45
a2_deg = -30
a3_deg = 45
a4_deg = -20

# Convert degrees to radians
a1 = np.radians(a1_deg)
a2 = np.radians(a2_deg)
a3 = np.radians(a3_deg)
a4 = np.radians(a4_deg)

# Set joint angles and lengths
joint_angles = [a1, a2, a3, a4]
joint_lengths = [l1, l2, l3, l4]

# ----------------------
# Forward Kinematics
# ----------------------


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


# Compute positions for the current configuration
target_positions = forward_kinematics(joint_angles, joint_lengths)

# ----------------------
# Plot Animation
# ----------------------

# Set up the animation
fig, ax = plt.subplots(figsize=(10, 6))
ax.xaxis.set_tick_params(labelsize=10)
ax.yaxis.set_tick_params(labelsize=10)
(line,) = ax.plot([], [], "o-", linewidth=3, markersize=8, color="blue", label="Arm")
(end_label,) = ax.plot([], [], "go", markersize=10, label="End Effector")
end_effector_text = ax.text(0, 0, "", color="green", fontsize=12, visible=True)


ax.set_xlim(0, 751)
ax.set_ylim(0, 751)
ax.set_aspect("equal")
ax.set_title("4-Joint Arm Forward Kinematics")
ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")


# More grid lines
tick_spacing = 50
ax.set_xticks(np.arange(0, 751, tick_spacing))
ax.set_yticks(np.arange(0, 751, tick_spacing))
ax.minorticks_on()
ax.grid(which="major", color="gray", linewidth=0.8)
ax.grid(which="minor", color="lightgray", linestyle=":", linewidth=0.5)

frames = 50
rest_angles = [0, 0, 0, 0]


def interpolate_angles(start_angles, end_angles, t):
    return [start + t * (end - start) for start, end in zip(start_angles, end_angles)]


def init():
    line.set_data([], [])
    end_label.set_data([], [])
    end_effector_text.set_text("")
    return line, end_label, end_effector_text


def animate(i):
    t = i / frames if i < frames else 1.0
    current_angles = interpolate_angles(rest_angles, joint_angles, t)
    positions = forward_kinematics(current_angles, joint_lengths)
    x_vals, y_vals = zip(*positions)

    line.set_data(x_vals, y_vals)

    # Update end effector (last joint) marker and label
    end_x, end_y = x_vals[-1], y_vals[-1]
    end_label.set_data([end_x], [end_y])
    end_effector_text.set_position((end_x + 10, end_y + 10))
    end_effector_text.set_text(f"({int(end_x)}, {int(end_y)})")

    return line, end_label, end_effector_text


ani = animation.FuncAnimation(
    fig, animate, frames=frames + 10, init_func=init, blit=True, interval=50
)

plt.tight_layout()
plt.show()
