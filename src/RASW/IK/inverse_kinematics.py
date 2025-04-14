"""Inverse Kinematics calculations for robotic arms."""

import math
from typing import Tuple, List, Optional


def calculate_ik(target_x: float, target_y: float, arm_lengths: List[float]) -> Tuple[Optional[List[float]], Optional[str]]:
    """Calculate inverse kinematics for a multi-joint planar robotic arm.
    
    Currently supports 2-link arms. Future versions will support n-link arms.
    
    Args:
        target_x: X-coordinate of the target position
        target_y: Y-coordinate of the target position
        arm_lengths: List of arm segment lengths (currently uses first two)
        
    Returns:
        Tuple containing:
        - List of joint angles in degrees, or None if target is unreachable
        - Error message if any, None otherwise
    """
    if len(arm_lengths) < 2:
        return None, "At least two arm segments are required"
    
    # Currently using just the first two segments
    L1, L2 = arm_lengths[0], arm_lengths[1]
    
    # Compute distance to target
    D = math.sqrt(target_x**2 + target_y**2)
    
    # Check if the point is reachable
    if D > (L1 + L2):
        return None, "Target is out of reach"
    elif D < abs(L1 - L2):
        return None, "Target is too close to reach"
    
    # Compute elbow angle using law of cosines
    cos_elbow_angle = (L1**2 + L2**2 - D**2) / (2 * L1 * L2)
    cos_elbow_angle = max(-1, min(1, cos_elbow_angle))  # Clamp to valid range
    elbow_angle = math.acos(cos_elbow_angle)
    
    # Compute shoulder angle
    target_angle = math.atan2(target_y, target_x)
    cos_alpha = (L1**2 + D**2 - L2**2) / (2 * L1 * D)
    cos_alpha = max(-1, min(1, cos_alpha))  # Clamp to valid range
    alpha = math.acos(cos_alpha)
    
    # There are two possible solutions (elbow up or down)
    # We choose the elbow-up solution here
    shoulder_angle = target_angle - alpha
    
    # Convert to degrees
    shoulder_angle_deg = math.degrees(shoulder_angle)
    elbow_angle_deg = math.degrees(elbow_angle)
    
    # Return joint angles in degrees
    return [shoulder_angle_deg, elbow_angle_deg], None 