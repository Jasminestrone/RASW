import numpy as np
from numpy import linalg as LA
import math


# Inputed variables
l1 = float(input("How long do you want your first arm to be?"))
l2 = float(input("How long do you want your second arm to be?"))
l3 = float(input("How long do you want your third arm to be?"))
l4 = float(input("How long do you want your fourth arm to be?"))
l1_angle = math.radians(
    float(input("What do you want the angle of your first arm to be at?"))
)
l2_angle = math.radians(
    float(input("What do you want the angle of your second arm to be at?"))
)
l3_angle = math.radians(
    float(input("What do you want the angle of your third arm to be at?"))
)
l4_angle = math.radians(
    float(input("What do you want the angle of your fourth arm to be at?"))
)


def rotate_vector(vector, angle):
    rotation_matrix = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    return np.dot(rotation_matrix, vector)


# Defineing arm vectors
arm_1_vect = np.array([l1, 0])
arm_2_vect = np.array([l2, 0])
arm_3_vect = np.array([l3, 0])
arm_4_vect = np.array([l4, 0])

# First joint position (0,0)
joint_1_pos = np.array([0, 0])

# Rotate first arm
arm_1_rotated = rotate_vector(arm_1_vect, l1_angle)
joint_2_pos = joint_1_pos + arm_1_rotated

# Rotate second arm
arm_2_rotated = rotate_vector(arm_2_vect, l1_angle + l2_angle)
joint_3_pos = joint_2_pos + arm_2_rotated

# make this a reverse step function so I can import how many arm lengths

# Rotate third arm
arm_3_rotated = rotate_vector(arm_3_vect, l1_angle + l2_angle + l3_angle)
joint_4_pos = joint_3_pos + arm_3_rotated

# Rotate fourth arm by
arm_4_rotated = rotate_vector(arm_4_vect, l1_angle + l2_angle + l3_angle + l4_angle)
end_effector_pos = joint_4_pos + arm_4_rotated

print("Joint 1 position:", joint_1_pos)
print("Joint 2 position:", joint_2_pos)
print("Joint 3 position:", joint_3_pos)
print("Joint 4 position:", joint_4_pos)
print("End effector position:", end_effector_pos)
