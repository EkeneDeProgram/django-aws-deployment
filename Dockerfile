# Use the official slim version of Python 3.10 as the base image.
FROM python:3.10-slim

# Set the working directory inside the container to /app.
WORKDIR /app

# Copy the requirements.txt file from your host machine to the /app directory in the container.
COPY requirements.txt ./

# Install Python packages listed in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code from the host into the container’s working directory (/app).
COPY . .

# Collect static files for Django (important for serving CSS, JS, etc.)
RUN python manage.py collectstatic --noinput

# Define the default command that runs when the container starts.
CMD ["gunicorn", "microservice.wsgi:application", "--bind", "0.0.0.0:8000"]
