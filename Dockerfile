# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# # Run the Django migrations 
# RUN python manage.py migrate

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME venv

# Run the Django application when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
