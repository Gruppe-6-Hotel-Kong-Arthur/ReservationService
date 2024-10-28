# Base image
FROM python:3.11-slim

# Copy alle filer i den mappe hvor min Dockerfile er til /app mappen i mit image
COPY . /app

# Skift til mappen /app (svarer til CD kommandoen)
WORKDIR /app

# Installer alle dependencies
RUN pip install -r requirements.txt

# Make port 5003 available to the world outside this container
EXPOSE 5003

# Eksekver denne kommando når Containeren køres
CMD ["python", "app.py"]