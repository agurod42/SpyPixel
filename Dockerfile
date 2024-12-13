FROM python:3.9-slim

WORKDIR /app

COPY . .

# Install dependencies
RUN pip install --no-cache-dir python-dotenv gunicorn\
    flask flask-login flask-bcrypt flask-sqlalchemy flask-migrate

EXPOSE 5000

# Run the Flask application with Gunicorn
CMD ["/app/run_app.sh"]
