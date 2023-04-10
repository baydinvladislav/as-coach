"""
Common application config
"""

import os

DATABASE_URL = os.environ.get("DATABASE_URL")
STATIC_DIR = os.path.join(os.getcwd(), "static")
