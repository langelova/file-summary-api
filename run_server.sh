#!/usr/bin/env bash
case "$1" in
dev*)
    echo Running as dev
    exec uvicorn api.main:app --host 0.0.0.0 --port 5000 --reload
  ;;
*)
    echo Running in prod
    exec gunicorn --bind :5000 --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 --timeout 0 api.main:app
  ;;
esac
