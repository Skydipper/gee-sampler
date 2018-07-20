#!/bin/bash
set -e

case "$1" in
    develop)
        echo "Running Development Server"
	echo -e "$EE_PRIVATE_KEY" | base64 -d > privatekey.pem
        exec python main.py
        ;;
    test)
        echo "Test"
        exec python test.py
        ;;
    start)
        echo "Running Start"
        exec gunicorn -c gunicorn.py gee_sampler:app
        ;;
    *)
        exec "$@"
esac
