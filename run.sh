#!/bin/bash
poetry install
echo "Port: $PORT"
poetry run gunicorn "app:create_app()" --bind 0.0.0.0:${PORT}