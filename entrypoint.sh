#!/bin/bash
# Wait for the PostgreSQL database to be ready
echo "⏳ Waiting for database to be ready..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "✅ Database is ready!"

# Apply migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
