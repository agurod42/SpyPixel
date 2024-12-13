FROM python:3.9-slim

WORKDIR /app

COPY . .

# Install dependencies
RUN pip install --no-cache-dir \
    flask \
    flask-bcrypt \
    flask-login \
    flask-migrate \
    flask-sqlalchemy \
    gunicorn \
    psycopg2-binary \
    python-dotenv

EXPOSE 5000

# Run the Flask application with Gunicorn
CMD ["/app/run_app.sh"]
