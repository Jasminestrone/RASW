
Math for 2D inverse kinematics

The elbow angle is found using the law of cosines where we do
https://latex.codecogs.com/svg.image?\cos(\theta_2)=\frac{L_1^2&plus;L_2^2-D^2}{2L_1L_2}
Then we can find the elbow angle using the equation
theta2 = cos^-1(cos(theta2))
This outputs the angle that the elbow arm needs to be at (where 0 degrees is fully extended
and 180 degrees is fully folded back)

Next we compute the shoulder angle in two steps:
1. First we find the angle from the origin to the target point:
   a = tan^-1(y/x)
2. Then we find the angle between the first link and the line to the target:
   cos(alpha) = (L1^2 + D^2 - L2^2) / (2*L1*D)
   alpha = cos^-1(cos(alpha))

Finally we get theta1 by subtracting alpha from the target angle:
theta1 = a - alpha

We convert these angles from radians to degrees by doing:
theta1_degs = theta1 * 180/pi and theta2_degs = theta2 * 180/pi