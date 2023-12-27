# Dockerfile

FROM python:3.9

ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
RUN mkdir /code

WORKDIR /api

# Copy the current directory contents into the container at /code/
COPY . /api/

# Set environment variables
ENV SECRET_KEY=foo
ENV DEBUG=0
ENV USE_SQLITE=0
ENV ALLOWED_HOSTS='localhost 127.0.0.1 0.0.0.0'
ENV DATABASE_NAME='drf_project'
ENV DATABASE_USER='postgres'
ENV DATABASE_PASSWORD='postgres'
ENV DATABASE_HOST='db'
ENV DATABASE_PORT=5432


# insatll all requirements
RUN pip install -r requirements.txt


# # Run makemigrations and migrate commands
# RUN python manage.py makemigrations
# RUN python manage.py migrate

# Make port 8000 available to the world outside this container

# # Define environment variable
# ENV NAME World

# # Run app.py when the container launches
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

