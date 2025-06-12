# Delineation Reader

An assignment for Philips Healthcare to process ECG delineation files and compute heart rate statistics.

## Getting Started

You can run the application using Docker (recommended) or set it up locally.

## Docker Setup (Recommended)

1. Build the Docker image:
```
   docker-compose build
```

2. Start the application:
```
   docker-compose up
```

3. Visit the app at:
```
   http://localhost:5000
```

## Local Setup

Requirements:
- Python 3.10
- Node.js ≥ v18

### Frontend

cd frontend
```
npm install
npm run build
```

Then manually copy the build/ folder contents into backend/static/:
```
cp -r build/* ../backend/static
```

### Backend
```
cd backend
pip install -r requirements.txt
python app.py
```

App will be available at
```
http://localhost:5000
```

## Running Tests

From the root of the project, run:
```
pytest
```

