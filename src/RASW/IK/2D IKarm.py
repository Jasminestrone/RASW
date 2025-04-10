import math
import numpy as np

def inverse_kinematics_3link(a, b, l1, l2, l3, offset):
    """
    Calculate joint angles for a 3-link robot arm to reach a target position (a,b)

    Parameters:
        a, b: Target position coordinates in inches
        l1, l2, l3: Lengths of the three arm links in inches
        offset: Angle offset for the first joint in degrees
        
    Returns:
        a1, a2, a3: Joint angles in degrees
    """
    # Convert offset to radians
    o = math.radians(offset)
    
    # Calculate first joint angle (a1)
    a1_rad = math.asin(b/a) + o
    
    # Calculate intermediate values needed for a2 and a3
    cos_a1_plus_o = math.cos(a1_rad)
    sin_a1_plus_o = math.sin(a1_rad)
    
    # Calculate the coordinates after the first joint
    b_minus_cos_term = b - cos_a1_plus_o * l1
    a_minus_sin_term = a - sin_a1_plus_o * l1
    
    # Calculate the distance from joint 1 to target
    d = math.sqrt(b_minus_cos_term**2 + a_minus_sin_term**2)
    
    # Calculate second joint angle (a2)
    term1 = math.asin(b_minus_cos_term / d)
    term2 = math.acos((l3**2 - d**2 - l2**2) / (-2 * d * l2))
    term3 = (180 - math.degrees(math.asin(b/a)) - offset)
    
    a2_rad = term1 + term2 + math.radians(term3)
    
    # Calculate third joint angle (a3)
    a3_rad = math.acos((d**2 - l3**2 - l2**2) / (-2 * l3 * l2))
    
    # Convert to degrees
    a1_deg = math.degrees(a1_rad)
    a2_deg = math.degrees(a2_rad)
    a3_deg = math.degrees(a3_rad)
    
    return a1_deg, a2_deg, a3_deg

def forward_kinematics_3link(a1, a2, a3, l1, l2, l3):
    """
    Calculate the end effector position for a 3-link robot arm given joint angles
    
    Parameters:
        a1, a2, a3: Joint angles in degrees
        l1, l2, l3: Lengths of the three arm links in inches
        
    Returns:
        x, y: End effector position in inches
    """
    # Convert angles to radians
    a1_rad = math.radians(a1)
    a2_rad = math.radians(a2)
    a3_rad = math.radians(a3)
    
    # Calculate the end position
    x1 = l1 * math.sin(a1_rad)
    y1 = l1 * math.cos(a1_rad)
    
    x2 = x1 + l2 * math.sin(a1_rad + a2_rad)
    y2 = y1 + l2 * math.cos(a1_rad + a2_rad)
    
    x3 = x2 + l3 * math.sin(a1_rad + a2_rad + a3_rad)
    y3 = y2 + l3 * math.cos(a1_rad + a2_rad + a3_rad)
    
    return x3, y3

# Example usage
if __name__ == "__main__":
    # Example parameters (all lengths in inches)
    l1 = 4.0  # Length of first link in inches
    l2 = 4.0  # Length of second link in inches
    l3 = 4.0  # Length of third link in inches
    offset = 0  # Offset angle in degrees
    
    # Target position in inches
    a = 8.0  # x-coordinate in inches
    b = 6.0  # y-coordinate in inches
    
    try:
        # Calculate joint angles
        a1, a2, a3 = inverse_kinematics_3link(a, b, l1, l2, l3, offset)
        
        print(f"Target position: ({a} inches, {b} inches)")
        print(f"Joint angles: a1={a1:.2f}°, a2={a2:.2f}°, a3={a3:.2f}°")
        
        # Verify with forward kinematics
        x, y = forward_kinematics_3link(a1, a2, a3, l1, l2, l3)
        print(f"Forward kinematics check: ({x:.2f} inches, {y:.2f} inches)")
        print(f"Error: {math.sqrt((x-a)**2 + (y-b)**2):.4f} inches")
        
    except Exception as e:
        print(f"Error in calculation: {e}")
        print("The target position might be unreachable with the given link lengths.")
        
    # Check the reachable workspace
    print("\nReachable workspace:")
    min_reach = max(0, abs(l1 - l2 - l3))  # Minimum reach
    max_reach = l1 + l2 + l3  # Maximum reach
    print(f"Minimum reach: {min_reach:.2f} inches")
    print(f"Maximum reach: {max_reach:.2f} inches")
