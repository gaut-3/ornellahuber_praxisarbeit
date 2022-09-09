#!/usr/bin/env bash

# Run a WSGI server to serve the application.
# gunicorn must be declared as a dependency in requirements.txt.
# Alternatively, one can try to use --worker-class=gevent (which has to be included in the requirements.txt)
# timeout = 6 hours (just in case there are some super very long lasting model training

export FLASK_APP=main.py
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

gunicorn -b :8080 main:app --timeout=21600 --workers=1 --log-level=debug

