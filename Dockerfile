# Use Python as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies and Ansible
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ansible \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port Streamlit will run on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
