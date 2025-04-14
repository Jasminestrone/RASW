from RASW import calculate_fk, calculate_ik
import RASW

print(f"RASW module loaded from: {RASW.__file__}")
import inspect

print(f"calculate_ik function source: {inspect.getsource(calculate_ik)}")

# Forward Kinematics example
arm_lengths = [160, 160, 160, 160]  # Four arm segments
joint_angles = [45, -30, 60, 35]  # Joint angles in degrees
joint_positions, error = calculate_fk(arm_lengths, joint_angles)

if not error:
    base_pos = joint_positions[0]
    end_effector_pos = joint_positions[-1]
    print(f"End effector at: ({end_effector_pos[0]:.2f}, {end_effector_pos[1]:.2f})")

# Inverse Kinematics example
target_x, target_y = 200, 150
arm_lengths = [160, 160, 160]  # Three arm segments
joint_angles, error = calculate_ik(target_x, target_y, arm_lengths)

if not error:
    shoulder_angle = joint_angles[0]
    elbow_angle = joint_angles[1]
    wrist_angle = joint_angles[2]
    print(
        f"Shoulder angle: {shoulder_angle:.2f}°, Elbow angle: {elbow_angle:.2f}°, Wrist angle : {wrist_angle:.2f}°"
    )
