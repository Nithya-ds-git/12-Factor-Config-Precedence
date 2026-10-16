#!/bin/bash
cd "$(dirname "$0")"
pip install -r requirements.txt
export APP_WORKERS=7
echo "Open: http://localhost:8080/effective-config"
python -m uvicorn main:app --port 8080
