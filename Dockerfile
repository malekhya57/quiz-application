# Use an official Python runtime as a parent image.
FROM python:3.10-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements.txt file to the container.
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code to the container.
COPY . .

# Expose the port your app uses (adjust if necessary).
EXPOSE 5000

# Command to run your application.
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]