FROM ubuntu:24.04

# Install necessary packages
RUN apt update && apt install -y \
    git \
    python3.12 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Create a virtual environment and activate it
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for data and models
RUN mkdir -p /app/data

# Copy the training script and utility functions into the container
COPY utils.py .
COPY train.py .

ENTRYPOINT ["python", "train.py"]
