"""Small, explicitly bounded exercises for the Gali-Maze SiV study."""

import os
import tempfile
from pathlib import Path

# Keep first-run font caches out of the user's global Python configuration.
os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "siv-study-matplotlib"))

__version__ = "0.1.0"
