#!/bin/env bash

export FLASK_APP=src/spy.py

# Run the database migrations
python -m flask db init
python -m flask db migrate -m "initial migration"
python -m flask db upgrade

# CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.spy:app", "--access-logfile", "-", "--error-logfile", "-"]
gunicorn -b 0.0.0.0:5000 src.spy:app --access-logfile - --error-logfile -
