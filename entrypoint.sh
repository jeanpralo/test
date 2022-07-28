#!/bin/bash

. venv_docker/bin/activate

export PYTHONPATH=$PYTHONPATH:.

alembic upgrade head

echo "Starting Challenge"
python fergus/app.py
