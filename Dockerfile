# Use Python 3.11 slim as the base image
FROM python:3.11-slim

# Copy all files from the directory
COPY . /app

# Change the working directory to /app (similar to the 'cd' command in a terminal)
WORKDIR /app

# Install all dependencies listed in the requirements.txt file
RUN pip install -r requirements.txt

# Make port 5003 available for connections from outside the container
EXPOSE 5003

# Run this command when the container starts
CMD ["python", "app.py"]
