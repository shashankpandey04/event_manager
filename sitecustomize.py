from pathlib import Path
import sys

base_dir = Path(__file__).resolve().parent
project_dir = base_dir / "event_manager"
project_dir_str = str(project_dir)
if project_dir_str not in sys.path:
    sys.path.insert(0, project_dir_str)
