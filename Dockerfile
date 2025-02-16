# Use an official Python image as base
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the monitoring script
CMD ["python", "restart_heroku.py"]
