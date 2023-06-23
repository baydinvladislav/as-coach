#!/bin/bash

echo '--Apply migrations--'
alembic upgrade head

echo '--Create user avatar folder--'
mkdir static/user_avatar

echo '--Start server--'
uvicorn src.main:app --host 0.0.0.0 --port 8000
