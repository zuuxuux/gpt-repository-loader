# Start from a base that has Python *and* Node, or install Node in python:3.13-slim
# For simplicity, let's pick python:3.13-slim and manually install Node.
FROM python:3.13-slim

# 1) Install system dependencies for both Python & Node
RUN apt-get update && apt-get install -y \
    nodejs npm \
    netcat-traditional \
    default-mysql-client \
    # Required dependencies for Playwright
    # libnss3 \
    # libnspr4 \
    # libatk1.0-0 \
    # libatk-bridge2.0-0 \
    # libcups2 \
    # libdrm2 \
    # libxkbcommon0 \
    # libxcomposite1 \
    # libxdamage1 \
    # libxfixes3 \
    # libxrandr2 \
    # libgbm1 \
    # libasound2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) Copy and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copy your entire backend code
COPY backend/ ./backend

# install noovox
WORKDIR /app/backend
RUN pip install .

# 4) Copy your frontend code
#    If your frontend is in a folder named 'frontend'
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# (Optional) Install Playwright, if you want to run E2E tests here
RUN npm install -g playwright
RUN npx playwright install
RUN npx playwright install-deps 

COPY frontend/ ./
RUN npm run build

# 5) Copy the built frontend into your Python backend’s static directory
WORKDIR /app
RUN mkdir -p noovox/static_frontend
RUN cp -R /app/frontend/dist/* noovox/static_frontend

# 6) (Optional) If you have a Python package for the backend, install it
# RUN pip install --no-cache-dir -e ./backend

# Expose the Flask port
EXPOSE 5000

# 7) Default command: run your Flask server
CMD ["python", "backend/app.py"]
