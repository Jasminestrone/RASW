# RASW
### Robotic Arm Software Package

| Description |

## Installation

<details>
<summary><h2>Installing pip (if needed)</h2></summary>
<details>
<summary>Windows</summary>
```
py -m ensurepip --default-pip
```
</details>
<details>
<summary>Mac/Linux</summary>
```
python3 -m ensurepip --default-pip
```
</details>
</details>

### <b>With pip installed</b>
```
pip install rasw
```
<details open>
<summary><h1>Math</h1></summary>
<h3>Math for 2D inverse kinematics</h3>

The elbow angle is found using the law of cosines where we do
    $$\cos(\theta_2) = \frac{L_1^2 + L_2^2 - D^2}{2L_1L_2}$$
Then we can find the elbow angle using the equation
    $$\theta_2 = \cos^{-1}(\cos(\theta_2))$$
This outputs the angle that the elbow arm needs to be at (where 0 degrees is fully extended and 180 degrees is fully folded back)

Next we compute the shoulder angle in two steps:
1. First we find the angle from the origin to the target point:
   $$\alpha = \tan^{-1}\left(\frac{y}{x}\right)$$
2. Then we find the angle between the first link and the line to the target:
   $$\cos(\alpha) = \frac{L_1^2 + D^2 - L_2^2}{2L_1D}$$
   $$\beta = \cos^{-1}(\cos(\beta))$$

Finally we get theta1 by subtracting alpha from the target angle:
    $$\theta_1 = \alpha - \beta$$

We convert these angles from radians to degrees by doing:
    $$\theta_1^{\circ} = \theta_1 \cdot \frac{180}{\pi}$$ and $$\theta_2^{\circ} = \theta_2 \cdot \frac{180}{\pi}$$

<h3>Math for 2D forward kinematics</h3>

| Math |
</details>