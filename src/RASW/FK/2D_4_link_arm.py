import numpy as np
from numpy import linalg as LA
import math

point_x = 5
point_y = 2
l1 = 160
l2 = 160
l3 = 160
l4 = 5
l1_angle = math.radians(40)
l2_angle = math.radians(-35)
l3_angle = math.radians(73)
l4_angle = math.radians(20)


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
