# Use Python 3.12 for better performance and compatibility
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=7860 \
    UV_SYSTEM_PYTHON=1 \
    HOME=/home/user \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_HEADLESS=true

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    git \
    tor \
    tor-geoipdb \
    netcat-traditional \
    curl \
    build-essential \
    python3-dev \
    libffi-dev \
    procps \
    nginx \
    # Browser dependencies for Playwright/Patchright
    libglib2.0-0 \
    libnspr4 \
    libnss3 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libcairo2 \
    libpango-1.0-0 \
    libasound2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set up working directory
WORKDIR /app

# Copy requirements and install as root
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt
RUN uv pip install --system fastapi uvicorn

# Install patchright browser
RUN patchright install chromium

# Create a non-root user
RUN useradd -m -u 1000 user
RUN mkdir -p /home/user/.streamlit && chown -R user:user /home/user

# Configure Tor
RUN echo "SocksPort 9050" >> /etc/tor/torrc && \
    echo "ControlPort 9051" >> /etc/tor/torrc && \
    echo "CookieAuthentication 1" >> /etc/tor/torrc && \
    echo "DataDirectory /var/lib/tor" >> /etc/tor/torrc

# Set permissions for Tor, app directory, and nginx
RUN mkdir -p /var/lib/tor && \
    chown -R user:user /var/lib/tor && \
    chmod 700 /var/lib/tor && \
    chown -R user:user /app && \
    mkdir -p /var/log/nginx /var/lib/nginx /tmp && \
    chown -R user:user /var/log/nginx /var/lib/nginx /tmp

# Copy the rest of the application
COPY --chown=user:user . .

# Set permissions for the start script
RUN chmod +x start.sh

# Switch to non-root user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Expose port
EXPOSE 7860

# Set the entrypoint
ENTRYPOINT ["./start.sh"]
