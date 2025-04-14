"""RASW - Robotic Arm Software Package."""

__version__ = "0.1.0"

# Import main functionality
from RASW.FK import calculate_fk
from RASW.IK import calculate_ik

# Expose key functions at the package level
__all__ = ["calculate_fk", "calculate_ik"]
