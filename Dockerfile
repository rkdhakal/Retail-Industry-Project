# Use Python as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies including Docker CLI, Ansible, and sudo
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    docker.io \
    ansible \
    git \
    sudo \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user with Docker permissions
RUN groupadd -f docker && \
    useradd -r -m -s /bin/bash -G docker dockeruser || echo "User already exists"

# Allow the user to use sudo without a password
RUN echo "dockeruser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set the environment variable for Docker CLI
ENV DOCKER_HOST=unix:///var/run/docker.sock

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Switch to the non-root user
USER dockeruser

# Expose the port Streamlit will run on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
