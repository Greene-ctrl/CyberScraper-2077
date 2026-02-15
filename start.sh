#!/bin/bash

# Start Tor service in the background
echo "Starting Tor..."
tor &

# Wait for Tor to start
sleep 5

# Start FastAPI API in the background
echo "Starting FastAPI API..."
python3 api.py &

# Start Streamlit app in the background
echo "Starting Streamlit..."
streamlit run main.py --server.port 8501 --server.address 0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false &

# Start Nginx in the foreground to keep the container running
echo "Starting Nginx..."
/usr/sbin/nginx -c /app/nginx.conf -g "daemon off;"
