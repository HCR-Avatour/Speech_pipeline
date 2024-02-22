# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code to the container
COPY app.py .

# Expose the port on which the Flask server will run
EXPOSE 5000

# Set the command to run the Flask server
CMD ["python", "app.py"]
