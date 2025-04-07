import math

# Arm lengths
L1 = 160
L2 = 160


def arm_math(x, y, L1, L2):
    # Compute distance to target
    D = math.sqrt(x**2 + y**2)

    # Check if the point is reachable
    if D > (L1 + L2):
        print("Target is out of reach")
        return None, None
    elif D < abs(L1 - L2):
        print("Target is too close to reach")
        return None, None

    # Compute elbow angle
    cos_elbow_angle = (L1**2 + L2**2 - D**2) / (2 * L1 * L2)
    cos_elbow_angle = max(-1, min(1, cos_elbow_angle))
    elbow_angle = math.acos(cos_elbow_angle)

    # Compute shoulder angle
    target_angle = math.atan2(y, x)
    cos_alpha = (L1**2 + D**2 - L2**2) / (2 * L1 * D)
    cos_alpha = max(-1, min(1, cos_alpha))
    alpha = math.acos(cos_alpha)

    # There are two possible solutions (elbow up or down)
    # We choose the elbow-up solution here
    shoulder_angle = target_angle - alpha

    # Convert to degrees
    shoulder_angle_deg = math.degrees(shoulder_angle)
    elbow_angle_deg = math.degrees(elbow_angle)

    return shoulder_angle_deg, elbow_angle_deg


# Inputs
x_target = float(input("What is your x target?"))
y_target = float(input("What is your y target?"))

shoulder_angle, elbow_angle = arm_math(x_target, y_target, L1, L2)
print(f"Shoulder Angle: {shoulder_angle:.2f} degrees")
print(f"Elbow Angle: {elbow_angle:.2f} degrees")


# How the math works

# The elbow angle is found using the law of cosines where we do
# cos(theta2) = (L1^2 + L2^2 - D^2) / (2*L1*L2)
# Then we can find the elbow angle using the equation
# theta2 = cos^-1(cos(theta2))
# This outputs the angle that the elbow arm needs to be at (where 0 degrees is fully extended
# and 180 degrees is fully folded back)

# Next we compute the shoulder angle in two steps:
# 1. First we find the angle from the origin to the target point:
#    a = tan^-1(y/x)
# 2. Then we find the angle between the first link and the line to the target:
#    cos(alpha) = (L1^2 + D^2 - L2^2) / (2*L1*D)
#    alpha = cos^-1(cos(alpha))

# Finally we get theta1 by subtracting alpha from the target angle:
# theta1 = a - alpha

# We convert these angles from radians to degrees by doing:
# theta1_degs = theta1 * 180/pi and theta2_degs = theta2 * 180/pi
