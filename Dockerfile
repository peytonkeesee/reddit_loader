# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

COPY .env .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the reddit_scraper.py script into the container
COPY reddit_scraper.py .

COPY utilities.py .  

# Set the script as the entrypoint
ENTRYPOINT ["python", "reddit_scraper.py"]