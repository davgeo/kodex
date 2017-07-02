#!/bin/bash

# Change to directory containing manage.py
cd ../kodex/

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
