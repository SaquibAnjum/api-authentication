"""Vercel entrypoint for the API Security Flask app."""

import sys
import os

# Ensure the src directory is on the path so the package can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api_security import app  # noqa: F401 – Vercel expects `app` in this module