#!/bin/bash
set -e

gunicorn \
  --workers 8 \
  --bind 0.0.0.0:5000 \
  --log-level debug \
  wsgi:app
