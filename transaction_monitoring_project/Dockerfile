# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variable for unbuffered output
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Define the command to run your app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
