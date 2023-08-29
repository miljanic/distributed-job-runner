#!/bin/sh
set -e

# TODO: Run migrations

exec uvicorn djb_api.run:app --host 0.0.0.0 --port 9000 --workers 4 --reload
