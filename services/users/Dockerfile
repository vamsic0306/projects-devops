# dockerfile
###############################################################
# USERS SERVICE DOCKERFILE
# Python + Flask + Gunicorn
###############################################################

FROM python:3.11-slim

# Work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose service port
EXPOSE 5001

# Start app using Gunicorn (production server)
CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]
