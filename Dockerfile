FROM python:3.11-slim

# Install dependencies: ffmpeg for audio conversion, unrar/rar, and build tools
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir flask yt_dlp

# Expose Flask default port
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]
