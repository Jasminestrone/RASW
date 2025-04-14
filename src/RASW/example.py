#!/usr/bin/env python
"""Example usage of RASW library functions."""

from RASW import calculate_fk, calculate_ik


def forward_kinematics_example():
    """Example of forward kinematics calculation."""
    print("\n=== Forward Kinematics Example ===")
    
    # Define arm lengths and joint angles
    arm_lengths = [160, 160, 160]  # Three arm segments of 160 units each
    joint_angles = [45, -30, 60]   # Joint angles in degrees
    
    # Calculate forward kinematics
    joint_positions, error = calculate_fk(arm_lengths, joint_angles)
    
    if error:
        print(f"Error: {error}")
    else:
        print("Arm configuration:")
        print(f"  Lengths: {arm_lengths}")
        print(f"  Angles: {joint_angles}")
        print("\nResults:")
        
        for i, pos in enumerate(joint_positions):
            if i == 0:
                print(f"  Base position: ({pos[0]:.2f}, {pos[1]:.2f})")
            elif i == len(joint_positions) - 1:
                print(f"  End effector position: ({pos[0]:.2f}, {pos[1]:.2f})")
            else:
                print(f"  Joint {i} position: ({pos[0]:.2f}, {pos[1]:.2f})")


def inverse_kinematics_example():
    """Example of inverse kinematics calculation."""
    print("\n=== Inverse Kinematics Example ===")
    
    # Define target position and arm lengths
    target_x, target_y = 200, 150
    arm_lengths = [160, 160]  # Two arm segments of 160 units each
    
    # Calculate inverse kinematics
    joint_angles, error = calculate_ik(target_x, target_y, arm_lengths)
    
    if error:
        print(f"Error: {error}")
    elif joint_angles:
        print("Target position:")
        print(f"  X: {target_x}, Y: {target_y}")
        print(f"  Arm lengths: {arm_lengths}")
        print("\nResults:")
        
        for i, angle in enumerate(joint_angles):
            print(f"  Joint {i+1} angle: {angle:.2f} degrees")
    else:
        print("No solution found.")


if __name__ == "__main__":
    forward_kinematics_example()
    inverse_kinematics_example()