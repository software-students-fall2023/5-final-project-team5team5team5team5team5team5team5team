# Use an official Python runtime as a parent image
FROM python:3.11-slim


# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app/web_app
COPY requirements.txt /app/web_app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/web_app/requirements.txt

# Copy the rest of the application's code into the container at /app/web_app
COPY . /app/web_app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Change the work directory to /app/web_app where app.py is located
WORKDIR /app/web_app

# Run app.py when the container launches
CMD ["python", "app.py"]
