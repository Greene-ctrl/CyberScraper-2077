#!/bin/bash

# Start Tor service in the background
echo "Starting Tor..."
tor &

# Wait for Tor to start (minimal wait, it bootstraps in background)
sleep 2

# Start FastAPI API in the background
echo "Starting FastAPI API..."
python3 api.py &

# Start Streamlit app in the background
echo "Starting Streamlit..."
# Ensure we use the right port and address
python3 -m streamlit run main.py --server.port 8501 --server.address 0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false &

# Wait for Streamlit to at least start
sleep 5

# Start Nginx in the foreground to keep the container running
echo "Starting Nginx..."
# Use the config we provided
/usr/sbin/nginx -c /app/nginx.conf -g "daemon off;"
