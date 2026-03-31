# =====================================================================
# Dockerfile for Wine Price Prediction Flask App
# =====================================================================
# This file contains instructions for Docker to build a container image
# for your Flask application
# =====================================================================

# =====================================================================
# STEP 1: SPECIFY BASE IMAGE
# =====================================================================
# Start from official Python 3.7.16 image
# This image has Python 3.7.16 pre-installed
# Alpine is a lightweight Linux distribution (~40MB vs 900MB)
# Using Alpine keeps the image small and fast
FROM python:3.7.16-slim

# =====================================================================
# STEP 2: SET WORKING DIRECTORY
# =====================================================================
# Create and set the working directory inside the container
# This is like "cd /app" - all commands run from this directory
WORKDIR /app

# =====================================================================
# STEP 3: COPY REQUIREMENTS FILE
# =====================================================================
# Copy requirements.txt from your machine (local) to container
# COPY <from_local_path> <to_container_path>
COPY requirements.txt .

# =====================================================================
# STEP 4: INSTALL DEPENDENCIES
# =====================================================================
# Install all Python packages from requirements.txt using pip
# The -r flag means "read from file"
# This ensures all dependencies are in the container
RUN pip install --no-cache-dir -r requirements.txt

# =====================================================================
# STEP 5: COPY APPLICATION FILES
# =====================================================================
# Copy your Flask app code to the container
COPY app.py .

# Copy templates folder (HTML files)
COPY templates/ ./templates/

# Copy trained model files
COPY models/ ./models/

# =====================================================================
# STEP 6: EXPOSE PORT
# =====================================================================
# Tell Docker that the app listens on port 5000
# This documents which port the app uses (doesn't actually open it)
# The actual port opening happens in docker-compose.yml
EXPOSE 5000

# =====================================================================
# STEP 7: SET ENVIRONMENT VARIABLES
# =====================================================================
# Disable Python from buffering output - see logs in real-time
ENV PYTHONUNBUFFERED=1

# Set Flask to production mode
ENV FLASK_ENV=production

# =====================================================================
# STEP 8: DEFINE STARTUP COMMAND
# =====================================================================
# CMD specifies what command runs when the container starts
# This is like running: gunicorn app:app
# The app will start when you run: docker run
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# =====================================================================
# SUMMARY OF DOCKERFILE
# =====================================================================
# 
# This Dockerfile:
# 1. Starts with Python 3.7.16 base image
# 2. Creates /app directory inside container
# 3. Installs all Python packages
# 4. Copies your Flask code
# 5. Exposes port 5000
# 6. Runs gunicorn server on startup
# 
# When you build this: Creates a Docker image
# When you run this: Creates a Docker container
# 
# =====================================================================
