import sys
import os

# Add the 'src' directory to sys.path so api_security module is found
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from api_security import app
