# === React Frontend Build Stage ===
FROM node:18-alpine AS frontend

WORKDIR /app
COPY ./frontend .
RUN npm install
RUN npm run build

# === Flask Backend Stage ===
FROM python:3.10-slim

WORKDIR /app
COPY ./backend ./backend
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy React build into Flask static folder
COPY --from=frontend /app/build /app/backend/static

WORKDIR /app/backend
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]