#!/bin/bash

# Train the model
python train.py --config config.yaml

# Start the FastAPI server
uvicorn app:app --host 0.0.0.0 --port 8000
