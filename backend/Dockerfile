# Use an official Python runtime as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'fyp.settings.prod'

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock into the container at /app
COPY Pipfile Pipfile.lock /app/

# Install pipenv and project dependencies
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy the application code into the container at /app
COPY . /app/

# Collect static files
RUN pipenv run python manage.py collectstatic --noinput

# Expose the port that Gunicorn will use
EXPOSE 8000

# Start Gunicorn server
CMD ["sh", "-c", "pipenv run python manage.py migrate && pipenv run gunicorn --bind 0.0.0.0:8000 --workers=2 fyp.wsgi:application"]
# CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "fyp.wsgi:application"]
