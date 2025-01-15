FROM python:3.13-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables
ENV FLASK_APP=src.main
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 7012

# Run the application
CMD ["python", "-m", "src.main"]