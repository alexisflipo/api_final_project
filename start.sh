#!/bin/bash
python3 ./ml_scripts/get_data.py
uvicorn app:app --host 0.0.0.0 --port $PORT