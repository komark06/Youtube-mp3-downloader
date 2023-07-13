#!/bin/sh

# Calculate the number of Gunicorn workers
CORES=$(nproc)
WORKERS=$((CORES * 2 + 1))

# Start Gunicorn with the specified number of workers
exec gunicorn -b 0.0.0.0:8080 --backlog 1 --workers $WORKERS --threads 1 --graceful-timeout 0 --timeout 0 app:app
