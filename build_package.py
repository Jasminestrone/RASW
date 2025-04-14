#!/usr/bin/env python
"""Build and publish the RASW package."""

import os
import subprocess
import sys
import glob
import platform


def run_command(command):
    """Run a shell command and print output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=False)
    return result.returncode


def main():
    """Main build function."""
    print("Building RASW package...")

    # Clean previous builds
    if os.path.exists("dist"):
        if platform.system() == "Windows":
            run_command("rmdir /s /q dist")
        else:
            run_command("rm -rf dist")

    # Install build dependencies
    run_command("pip install --upgrade pip")
    run_command("pip install --upgrade build twine")

    # Build package
    build_result = run_command("python3 -m build")
    if build_result != 0:
        print("Error building package")
        return build_result

    # Find the wheel file
    wheel_files = glob.glob(os.path.join("dist", "*.whl"))
    if wheel_files:
        wheel_file = wheel_files[0]
        print(f"\nWheel file created: {wheel_file}")
    else:
        print("\nWarning: No wheel file found in the dist directory.")
        print("The build process may have failed to create a wheel.")
        wheel_file = ""


if __name__ == "__main__":
    sys.exit(main())
