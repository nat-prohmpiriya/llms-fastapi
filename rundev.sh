#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(dirname "$0")
cd "$(dirname "$0")/app"
python -m pipenv run python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000