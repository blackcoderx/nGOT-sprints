# ETA Predictor

A FastAPI-based machine learning service that predicts delivery time (ETA) for logistics shipments in Ghana.

## What This Project Does

- **Input**: Pickup location, delivery location, cargo weight, departure time, vehicle type, etc.
- **Output**: Estimated delivery time in minutes
- **Used by**: Logistics/delivery applications

## Tech Stack

- **API**: FastAPI (Python web framework)
- **ML**: scikit-learn (Gradient Boosting model)
- **Experiment Tracking**: MLflow
- **Data Versioning**: DVC
- **Container**: Docker

## Project Structure

```
eta-predictor/
├── app/
│   ├── main.py        # FastAPI application (API endpoints)
│   ├── schemas.py     # Request/response validation models
│   └── predictor.py  # ML model loading & prediction
├── scripts/
│   ├── generate_data.py  # Create synthetic training data
│   ├── preprocess.py    # Prepare data for training
│   └── train.py        # Train ML model
├── tests/
│   ├── test_api.py      # API endpoint tests
│   └── test_schemas.py # Validation tests
├── data/               # Raw and processed data
├── models/             # Trained model files
├── dvc.yaml           # DVC pipeline definition
├── Dockerfile         # Container image definition
└── docker-compose.yml # Local development stack
```

## Quick Start (Local)

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Generate synthetic training data:
   ```bash
   python scripts/generate_data.py
   ```

3. Run the API:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Open http://localhost:8000/docs for interactive API documentation.

## Quick Start (Docker)

```bash
docker-compose up --build
```

- API: http://localhost:8000
- MLflow UI: http://localhost:5000

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict` | POST | Get ETA prediction |
| `/health` | GET | Check service status |
| `/docs` | GET | Interactive API docs |

## Example Request

```json
{
  "origin_lat": 5.6037,
  "origin_lon": -0.1870,
  "dest_lat": 6.6885,
  "dest_lon": -1.6244,
  "cargo_weight_kg": 500,
  "hour_of_day": 10,
  "day_of_week": 1
}
```

## Running Tests

```bash
poetry run pytest
```

```
poetry run python scripts/train.py
poetry run mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlflow-artifacts

```
