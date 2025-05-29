#!/bin/bash

# Navigate to the directory where the script is located (optional, but good practice)
# cd "$(dirname "$0")"

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install --no-cache-dir -r requirements.txt
else
    echo "requirements.txt not found. Skipping dependency installation."
    # Optionally, exit if requirements are critical
    # exit 1
fi

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found! Cannot start the application."
    exit 1
fi

# Run the Flask application using Gunicorn
# Gunicorn is a WSGI HTTP server for UNIX. It's a pre-fork worker model.
# We bind it to 0.0.0.0 to make it accessible from outside the container/machine.
# Port 9000 is specified as per requirements.
# The 'app:app' means Gunicorn should look for an object named 'app' in a Python module named 'app.py'.
echo "Starting Flask application on port 9000..."
exec gunicorn --workers 3 --bind 0.0.0.0:9000 app:app
