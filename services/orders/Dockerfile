# dockerfile
###############################################################
# ORDERS SERVICE DOCKERFILE
# Uses Gunicorn for production
###############################################################

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5002

CMD ["gunicorn", "-b", "0.0.0.0:5002", "app:app"]
