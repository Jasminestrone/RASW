#!/usr/bin/env python
"""Command-line interface for RASW."""

import argparse
import sys
from RASW import __version__, calculate_fk, calculate_ik


def main():
    """Main entry point for the RASW CLI."""
    parser = argparse.ArgumentParser(
        description="RASW - Robotic Arm Software Package"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"RASW {__version__}"
    )
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Forward kinematics command
    fk_parser = subparsers.add_parser("fk", help="Forward kinematics calculations")
    fk_parser.add_argument("--lengths", nargs="+", type=float, required=True, 
                          help="Arm segment lengths")
    fk_parser.add_argument("--angles", nargs="+", type=float, required=True, 
                          help="Joint angles in degrees")
    
    # Inverse kinematics command
    ik_parser = subparsers.add_parser("ik", help="Inverse kinematics calculations")
    ik_parser.add_argument("--position", nargs=2, type=float, required=True, 
                          help="Target position (x, y)")
    ik_parser.add_argument("--lengths", nargs="+", type=float, required=True,
                          help="Arm segment lengths")
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    if args.command == "fk":
        if len(args.lengths) != len(args.angles):
            print("Error: Number of arm lengths must match number of joint angles")
            return
        
        joint_positions, error = calculate_fk(args.lengths, args.angles)
        
        if error:
            print(f"Error: {error}")
        else:
            for i, pos in enumerate(joint_positions):
                if i == 0:
                    print(f"Base position: ({pos[0]:.2f}, {pos[1]:.2f})")
                elif i == len(joint_positions) - 1:
                    print(f"End effector position: ({pos[0]:.2f}, {pos[1]:.2f})")
                else:
                    print(f"Joint {i} position: ({pos[0]:.2f}, {pos[1]:.2f})")
    
    elif args.command == "ik":
        target_x, target_y = args.position
        joint_angles, error = calculate_ik(target_x, target_y, args.lengths)
        
        if error:
            print(f"Error: {error}")
        elif joint_angles:
            for i, angle in enumerate(joint_angles):
                print(f"Joint {i+1} angle: {angle:.2f} degrees")
        else:
            print("No solution found.")


if __name__ == "__main__":
    sys.exit(main()) 