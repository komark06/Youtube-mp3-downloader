#!/bin/sh

# Calculate the number of Gunicorn workers
CORES=$(nproc)
WORKERS=$((CORES * 2 + 1))

# Start Gunicorn with the specified number of workers
exec gunicorn --workers $WORKERS app:app
