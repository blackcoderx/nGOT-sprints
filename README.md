# AI/ML Projects

A collection of three FastAPI-based AI/ML projects, each solving a different domain problem.

## Projects

### ETA Predictor
Predicts delivery time (ETA) for logistics shipments in Ghana using a Gradient Boosting model.

- **Stack**: FastAPI, scikit-learn, MLflow, DVC, Docker
- **Key endpoint**: `POST /predict`
- **README**: [eta-predictor/README.md](eta-predictor/README.md)

### Medical RAG
Clinical question answering system grounded in medical guidelines. All answers cite source documents.

- **Stack**: FastAPI, LlamaIndex, Pinecone, OpenAI
- **Key endpoint**: `POST /ask`
- **Knowledge base**: Malaria, hypertension, and diabetes guidelines

### Product Recommender
Semantic product recommendations powered by vector similarity search. Supports natural language queries like "something cozy for rainy weather".

- **Stack**: FastAPI, Pinecone, OpenAI
- **Key endpoint**: `POST /recommend`

## Common Patterns

All projects share the same structure:
- **FastAPI** for the API layer
- **Poetry** for dependency management
- **Pytest** for testing
- Python 3.11+

## Quick Start

Each project follows the same setup:

```bash
cd <project-name>
poetry install
uvicorn app.main:app --reload
```

API docs are available at `http://localhost:8000/docs`.
