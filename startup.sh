#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Navigate to the app directory
# cd app || exit

# black . || exit

# Run the Uvicorn server
# uvicorn main:app --host 0.0.0.0 --port 8000
uvicorn main:app --host 0.0.0.0 --port 8000