# RASW
![](https://img.shields.io/badge/Python-grey?style=for-the-badge&logo=python)

### Robotic Arm Software Package

RASW is a Python library for simulating and controlling robotic arms. It provides both forward and inverse kinematics calculations for 2D robotic arms with multiple segments. Use RASW for robotics education, prototyping, or controlling physical robotic arm systems. The library offers a simple API with comprehensive math documentation.

## Installation

RASW can be easily installed via pip:

```bash
pip install rasw
```

That's it! After installation, you can use the CLI tool with:

```bash
rasw-cli --help
```

Or import the package in your Python code:

```python
from RASW import calculate_fk, calculate_ik

# Example usage
joint_positions, _ = calculate_fk([10, 10], [45, 45])
```

### Building from source

If you want to build from source:

1. Clone the repository
   ```bash
   git clone https://github.com/Jasminestrone/RASW.git
   cd RASW
   ```

2. Run the build script
   ```bash
   # On Windows
   python build_package.py
   
   # On Mac/Linux
   python3 build_package.py
   ```

3. Install locally (the script will show the exact path to use)
   ```bash
   # On Windows
   pip install dist\your_wheel_file.whl
   
   # On Mac/Linux
   pip install dist/*.whl
   ```

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

When you first import RASW after installation, it will automatically open the GitHub documentation page in your default web browser. If you want to disable this behavior, set the environment variable `RASW_NO_BROWSER=1` before importing the package.

## Usage

### Command-line Interface

After installation, you can use the `rasw-cli` command:

```bash
# Get help
rasw-cli --help

# Show version
rasw-cli --version

# Forward Kinematics
rasw-cli fk --lengths 160 160 160 --angles 45 -30 60

# Inverse Kinematics 
rasw-cli ik --position 200 150 --lengths 160 160
```

### Python Library

You can also use RASW directly in your Python code:

```python
from RASW import calculate_fk, calculate_ik

# Forward Kinematics example
arm_lengths = [160, 160, 160]  # Three arm segments
joint_angles = [45, -30, 60]   # Joint angles in degrees
joint_positions, error = calculate_fk(arm_lengths, joint_angles)

if not error:
    base_pos = joint_positions[0]
    end_effector_pos = joint_positions[-1]
    print(f"End effector at: ({end_effector_pos[0]:.2f}, {end_effector_pos[1]:.2f})")

# Inverse Kinematics example
target_x, target_y = 200, 150
arm_lengths = [160, 160]  # Two arm segments
joint_angles, error = calculate_ik(target_x, target_y, arm_lengths)

if not error:
    shoulder_angle = joint_angles[0]
    elbow_angle = joint_angles[1]
    print(f"Shoulder angle: {shoulder_angle:.2f}°, Elbow angle: {elbow_angle:.2f}°")
```

<details open>
<summary><h1>Math</h1></summary>
<h3>Math for 2D inverse kinematics</h3>
Inverse kinematics desmos - https://www.desmos.com/calculator/uyuilbk8go

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

The forward kinematics calculation starts with the initial arm segments at the origin pointing along the x-axis, then applies sequential rotations to find each joint position.

For each arm segment (L1, L2, L3, L4), we:
- Begin with a vector along the x-axis with magnitude equal to the link length:
  $$\{arm_vector} = [L_i, 0]$$

- Apply rotation matrices to transform each link vector:
$$
R(\theta) = \begin{bmatrix}
\cos(\theta) & -\sin(\theta) \\
\sin(\theta) & \cos(\theta)
\end{bmatrix}
$$
For each joint, the rotation angle is cumulative from previous joints:
- First joint rotates by $\theta_1$ = l1_angle
- Second joint rotates by $\theta_2$ = l1_angle + l2_angle
- Third joint rotates by $\theta_3$ = l1_angle + l2_angle + l3_angle
- Fourth joint rotates by $\theta_4$ = l1_angle + l2_angle + l3_angle + l4_angle

Each joint position is calculated by adding the rotated vector to the previous joint:
  $${joint_i_pos} = {joint_(i-1)_pos} + R(\theta_{\text{cum}}) \cdot {arm_i_vect}$$

This process is repeated sequentially until we reach the end effector position, which is the position after the last arm segment.

The rotation function `rotate_vector(vector, angle)` multiplies the vector by the rotation matrix to produce a new vector rotated by the specified angle:
  $${rotated_vector} = R(\theta) \cdot \text{vector}$$

This approach correctly implements forward kinematics for a 4-link planar arm by accumulating rotations and positions from the base to the end effector.

</details>
