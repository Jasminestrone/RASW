import math

# Arm lengths
L1 = 10
L2 = 10


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
# cos(theta2) = (D^2 - L1^2 - L2^2) / 2L1L2
# Then we can find the elbow angle usign the equation
# theta2 = cos^-1(cos(theta2))
# This outputs the angle that the eblow arm needs to be at

# Next we can compute the shoudler angle
# First we can break the problem into two different angles
# a = tan^-1(y/x) Which is the angle fro mthe origin to the target point
# b = tan^-1((L2 sin(theta2)) / (L1 + L2 cos(theta2))) Which is the internal angle being caused by the forearm
# Finnaly if we can get theta1 by doing
# theta1 = a - b

# Then simply we can convet these angles from radians to degrees by doing
# theta1_degs = theta1 * 180/pi and theta2_degs = theta2 * 180/pi
