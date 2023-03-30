#!/bin/bash

exec poetry run alembic upgrade head
