#!/bin/bash
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /home/logs/gunicorn.log
touch /home/logs/access.log
tail -n 0 -f /home/logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn nexus.wsgi:application \
    --name nexus \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --log-file=/home/logs/gunicorn.log \
    --access-logfile=/home/logs/access.log \
    "$@"
