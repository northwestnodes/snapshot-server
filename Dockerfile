# Use the official Python image
FROM python:3.12.7-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
#EXPOSE 8000

# Run the application with uvicorn
#CMD ["uvicorn", "ovh_firewall:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["snapshot_api.py"]