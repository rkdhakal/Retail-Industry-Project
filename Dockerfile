# Use Python as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies including Docker CLI and Ansible
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    docker.io \
    ansible \
    git \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user with permissions
RUN groupadd -g 999 docker && \
    useradd -r -u 999 -g docker dockeruser && \
    usermod -aG docker dockeruser

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
