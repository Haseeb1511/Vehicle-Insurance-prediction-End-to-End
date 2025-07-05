#python
FROM python:3.10-slim-buster

WORKDIR /app

# Environment variable: Don't write .pyc files(__pycache__)
ENV PYTHONDONTWRITEBYTECODE=1

# Environment variable: Enable output buffering (set to 1 for stdout to show immediately)
ENV PYTHONUNBUFFERED=1

#copy from host dit to workdir
COPY . .

# Install dependencies and upgrade the pip
RUN pip install --upgrade pip && \
    pip install --default-timeout=100 --retries=10  -r requirements.txt



# Expose port 5000 for Flask app
EXPOSE 5000

# Default command to run the app
CMD ["python", "app.py"]