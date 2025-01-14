# ---------------------------
# Stage 1: Build the front-end
# ---------------------------
FROM node:18 AS frontend-builder
WORKDIR /app-frontend

# Copy your front-end code
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build
# After build, you'll have a /app-frontend/dist folder

# ----------------------------------------
# Stage 2: Build the Python back-end image
# ----------------------------------------
FROM python:3.13-slim
WORKDIR /app

# Copy requirements early for caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire backend
COPY backend/ ./

# Copy the built front-end files from Stage 1 into Flask's static folder
COPY --from=frontend-builder /app-frontend/dist ./noovox/static_frontend

# If you have a setup.py or a pyproject.toml, you can install the back-end as a package:
RUN pip install --no-cache-dir .

EXPOSE 5000

CMD ["python", "app.py"]
