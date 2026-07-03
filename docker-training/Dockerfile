# Step 1: Use an official lightweight Python image as the base
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy our local app.py file into the container's /app directory
COPY app.py .

# Step 4: Tell Docker that the container will listen on port 5000
EXPOSE 5000

# Step 5: Specify the command to run when the container starts
CMD ["python", "app.py"]