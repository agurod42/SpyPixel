FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask gunicorn

EXPOSE 5000

# Run the Flask application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "spy:app", "--access-logfile", "-", "--error-logfile", "-"]