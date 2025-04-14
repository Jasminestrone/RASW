"""RASW - Robotic Arm Software Package."""

__version__ = "0.1.0"

# Import main functionality
from RASW.FK import calculate_fk
from RASW.IK import calculate_ik

# Expose key functions at the package level
__all__ = ["calculate_fk", "calculate_ik"]

# Check if this is the first import after installation
import os
import webbrowser
from pathlib import Path

def _open_docs_on_first_run():
    """Open documentation website on first run after installation."""
    first_run_marker = Path.home() / ".rasw_first_run"
    if not first_run_marker.exists():
        try:
            # Create the marker file to prevent opening on subsequent imports
            first_run_marker.touch(exist_ok=True)
            # Open the GitHub repository page
            webbrowser.open("https://github.com/Jasminestrone/RASW")
            print("Opening RASW documentation...")
        except Exception:
            # Silently fail if there's an issue opening the browser
            pass

# Only run in non-interactive mode and when not inside tests
if os.environ.get('RASW_NO_BROWSER') != '1' and not __name__.startswith('_'):
    _open_docs_on_first_run()
