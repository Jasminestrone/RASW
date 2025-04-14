"""Forward Kinematics calculations for robotic arms."""

import numpy as np
import math
from typing import List, Tuple, Optional


def rotate_vector(vector: np.ndarray, angle: float) -> np.ndarray:
    """Rotate a 2D vector by a given angle.

    Args:
        vector: A 2D numpy array representing the vector to rotate
        angle: Angle in radians

    Returns:
        The rotated vector
    """
    rotation_matrix = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    return np.dot(rotation_matrix, vector)


def calculate_fk(
    arm_lengths: List[float], joint_angles: List[float]
) -> Tuple[List[Tuple[float, float]], Optional[str]]:
    """Calculate forward kinematics for a multi-joint planar robotic arm.

    Args:
        arm_lengths: List of arm segment lengths
        joint_angles: List of joint angles in degrees

    Returns:
        Tuple containing:
        - List of joint positions (x, y coordinates) including the end effector
        - Error message if any, None otherwise
    """
    if len(arm_lengths) != len(joint_angles):
        return [], "Number of arm lengths must match number of joint angles"

    # Convert angles to radians
    angles_rad = [math.radians(angle) for angle in joint_angles]

    # First joint position at origin
    joint_positions = [(0.0, 0.0)]

    # Initialize cumulative angle
    cumulative_angle = 0.0

    # Calculate positions for each joint
    for i in range(len(arm_lengths)):
        # Update cumulative angle (this follows the good FK code approach)
        cumulative_angle += angles_rad[i]

        # Create arm vector and rotate it
        arm_vector = np.array([arm_lengths[i], 0.0])
        arm_rotated = rotate_vector(arm_vector, cumulative_angle)

        # Add rotated arm to previous joint position
        prev_joint = np.array(joint_positions[-1])
        new_joint = prev_joint + arm_rotated

        # Add new joint position to the list
        joint_positions.append((float(new_joint[0]), float(new_joint[1])))

    return joint_positions, None
