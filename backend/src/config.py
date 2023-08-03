"""
Common application config
"""

import os

DATABASE_URL = os.environ.get("DATABASE_URL")
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
STATIC_DIR = os.path.join(os.getcwd(), "static")
TEST_ENV = os.environ.get("TEST_ENV", 0)
