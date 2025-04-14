"""Inverse Kinematics calculations for robotic arms."""

import math
from typing import Tuple, List, Optional


def calculate_ik(
    target_x: float, target_y: float, arm_lengths: List[float]
) -> Tuple[Optional[List[float]], Optional[str]]:
    # Validate input
    if len(arm_lengths) < 2:
        return None, "At least two arm segments are required"

    # Explicitly check for 3-link case
    if len(arm_lengths) >= 3:
        return _calculate_ik_3link(target_x, target_y, arm_lengths)
    else:
        # Compute distance to target
        D = math.sqrt(target_x**2 + target_y**2)
        return _calculate_ik_2link(target_x, target_y, arm_lengths, D)


def _safe_arccos(x: float) -> float:
    """Safely calculate arccos by clamping input to valid range."""
    return math.acos(max(-1.0, min(1.0, x)))


def _safe_arcsin(x: float) -> float:
    """Safely calculate arcsin by clamping input to valid range."""
    return math.asin(max(-1.0, min(1.0, x)))


def _calculate_ik_2link(
    target_x: float, target_y: float, arm_lengths: List[float], D: float
) -> Tuple[Optional[List[float]], Optional[str]]:
    """Calculate IK for a 2-link arm."""
    L1, L2 = arm_lengths[0], arm_lengths[1]

    # Check if the point is reachable
    if D > (L1 + L2):
        return None, "Target is out of reach"
    elif D < abs(L1 - L2):
        return None, "Target is too close to reach"

    # Compute elbow angle using law of cosines
    cos_elbow_angle = (L1**2 + L2**2 - D**2) / (2 * L1 * L2)
    elbow_angle = _safe_arccos(cos_elbow_angle)

    # Compute shoulder angle
    target_angle = math.atan2(target_y, target_x)
    cos_alpha = (L1**2 + D**2 - L2**2) / (2 * L1 * D)
    alpha = _safe_arccos(cos_alpha)

    # We choose the elbow-up solution here
    shoulder_angle = target_angle - alpha

    # Convert to degrees
    shoulder_angle_deg = math.degrees(shoulder_angle)
    elbow_angle_deg = math.degrees(elbow_angle)

    return [shoulder_angle_deg, elbow_angle_deg], None


def _calculate_ik_3link(
    target_x: float, target_y: float, arm_lengths: List[float]
) -> Tuple[Optional[List[float]], Optional[str]]:
    """Calculate IK for a 3-link arm using approach from the second example."""
    L1, L2, L3 = arm_lengths[0], arm_lengths[1], arm_lengths[2]

    # Apply an offset to base rotation (10 degrees like in example)
    offset = math.radians(10)
    a1_weight = 1  # Weight for the first angle as in example

    # Calculate total arm length and distance to target
    total_arm_length = L1 + L2 + L3
    distance_to_point = math.sqrt(target_x**2 + target_y**2)

    # Check if target is reachable
    if distance_to_point > total_arm_length:
        return None, "Target is out of reach"

    # Angle1 is base rotation toward the point
    angle1 = a1_weight * math.atan2(target_y, target_x) + offset

    # Position of joint 2
    p2_x_point = math.cos(angle1) * L1
    p2_y_point = math.sin(angle1) * L1

    # h = distance from joint 2 to target point
    h = math.sqrt((target_x - p2_x_point) ** 2 + (target_y - p2_y_point) ** 2)

    # Check if joint 2 to target is reachable with L2 and L3
    if h > (L2 + L3) or h < abs(L2 - L3):
        return None, "Target cannot be reached with given joint configuration"

    # b = target y, d = joint 2 y
    b = target_y
    d = p2_y_point

    # Calculate angle2
    try:
        angle2 = -angle1 + (
            _safe_arccos((L3**2 - L2**2 - h**2) / (-2 * L2 * h))
            + _safe_arcsin((b - d) / h)
        )
    except ValueError:
        return None, "Mathematical error in angle calculation"

    # Calculate angle3
    try:
        angle3 = -math.pi + _safe_arccos((h**2 - L2**2 - L3**2) / (-2 * L2 * L3))
    except ValueError:
        return None, "Mathematical error in angle calculation"

    # Convert to degrees
    angle1_deg = math.degrees(angle1)
    angle2_deg = math.degrees(angle2)
    angle3_deg = math.degrees(angle3)

    return [angle1_deg, angle2_deg, angle3_deg], None
