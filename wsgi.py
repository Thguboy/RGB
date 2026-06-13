import sys
import os

# ─── IMPORTANT ────────────────────────────────────────────────────────────────
# Replace 'YourUsername' with your actual PythonAnywhere username
# Example: /home/thguboy/RGB
# ──────────────────────────────────────────────────────────────────────────────
project_home = '/home/YourUsername/RGB'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load .env file if present (install python-dotenv: pip install python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(project_home, '.env'))
except ImportError:
    pass

from app import application  # noqa: F401
