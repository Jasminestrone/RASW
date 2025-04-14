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
    build_result = run_command("python -m build")
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
    
    # Check if we should upload to PyPI
    if len(sys.argv) > 1 and sys.argv[1] == "--upload":
        print("\nUploading to PyPI...")
        # Use dist/* pattern but handle it platform-independently
        dist_files = os.path.join("dist", "*")
        upload_result = run_command(f"python -m twine upload {dist_files}")
        if upload_result != 0:
            print("Error uploading package")
            return upload_result
        
        print("\nPackage successfully uploaded to PyPI!")
        print("Users can now install it with: pip install rasw")
    else:
        print("\nPackage built successfully!")
        print("Run with --upload flag to publish to PyPI")
        if wheel_file:
            print(f"Or test locally with: pip install {wheel_file}")
        else:
            print("Or test locally with: pip install dist/*.whl (Linux/Mac)")
            print("Or test locally with: pip install path\\to\\wheelfile.whl (Windows)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 