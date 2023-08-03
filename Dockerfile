# Use the Python 3.6 base image on Alpine Linux
FROM python:3.6-alpine

# Set environment variables for the Flask app
ENV FLASK_APP flasky.py
ENV FLASK_CONFIG production

# Create a user named 'flasky' with the '-D' flag (no home directory)
RUN adduser -D flasky

# Switch to the 'flasky' user for subsequent commands
USER flasky

# Set the working directory to /home/flasky
WORKDIR /home/flasky

# Copy the requirements directory to the container
COPY requirements /home/flasky/requirements
# Set up a Python virtual environment and install dependencies
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

# Copy the 'app', 'migrations', 'flasky.py', 'config.py', and 'boot.sh' files to the container
COPY app app
COPY migrations migrations
COPY flasky.py config.py boot.sh ./

# Expose port 5000 to the outside world
EXPOSE 5000

# Set the entrypoint to execute the 'boot.sh' script
ENTRYPOINT ["./boot.sh"]
