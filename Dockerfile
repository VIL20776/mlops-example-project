FROM ubuntu:24.04
# If using CUDA, use the appropriate base image
# FROM nvidia/cuda:13.1.2-cudnn-devel-ubuntu24.04

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

# Copy the training script and any other necessary files
COPY *.py .

CMD ["bash", "-c", "python loader.py && python train.py"]