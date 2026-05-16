# Technical Report — 10-Day AI/ML Sprint

**Author:** Emmanuel Ziggah  
**Email:** ziggahemmanuel99@gmail.com  
**Date:** May 16, 2026  
**Sprint Repository:** https://github.com/blackcoderx/nGOT-sprints

---

## Executive Summary

This report documents the design, implementation, and technical architecture of three FastAPI-based AI/ML projects developed during a 10-day sprint. The projects span three distinct domains: logistics prediction, clinical decision support, and e-commerce recommendations. All projects share a common architectural foundation — FastAPI for the API layer, Poetry for dependency management, Pydantic for input validation, and Pytest for testing — while employing domain-specific technologies for their core ML/AI functionality.

---

## 1. ETA Predictor — Logistics Delivery Time Estimation

**GitHub Path:** `eta-predictor/`  
**Repo Link:** https://github.com/blackcoderx/nGOT-sprints/tree/main/eta-predictor

### 1.1 Problem Statement

Predict estimated delivery times (ETA) for logistics shipments in Ghana based on GPS coordinates, cargo details, vehicle type, and temporal factors.

### 1.2 Architecture

```
Client → FastAPI API → ETAPredictor (scikit-learn pipeline) → Response
                              ↑
                        joblib model file
```

### 1.3 Technology Stack

| Component | Technology |
|-----------|-----------|
| API Framework | FastAPI 0.136+ |
| ML Framework | scikit-learn 1.8+ |
| Experiment Tracking | MLflow 3.11+ |
| Data Versioning | DVC 3.67+ |
| Containerization | Docker + Docker Compose |
| Dependency Management | Poetry 2.0+ |
| Testing | Pytest 9.0+ + HTTPX |
| Code Quality | Black + Ruff |

### 1.4 ML Pipeline

**Data Generation:** Synthetic logistics data generated via `scripts/generate_data.py` with realistic Ghana-based GPS coordinates, cargo weights, and temporal patterns.

**Feature Engineering:**
- Haversine distance calculation from GPS coordinates
- Rush hour detection (7-9 AM, 5-7 PM)
- One-hot encoding for vehicle types (truck, van, motorcycle)
- Cross-field validation (motorcycle weight limit of 100kg)

**Models Compared:**

| Model | Hyperparameters | Purpose |
|-------|----------------|---------|
| Gradient Boosting Regressor | n_estimators=200, lr=0.05, max_depth=4 | Baseline |
| Gradient Boosting Regressor | n_estimators=500, lr=0.03, max_depth=4 | More trees |
| Gradient Boosting Regressor | n_estimators=200, lr=0.05, max_depth=6 | Deeper trees |
| Random Forest | n_estimators=200, max_depth=10 | Comparison |
| Ridge Regression | alpha=1.0 | Linear baseline |

**Evaluation Metrics:** MAE, RMSE, R², MAPE, 5-fold cross-validation

**Pipeline:** `StandardScaler → Regressor` via scikit-learn Pipeline

### 1.5 MLOps Practices

- **MLflow:** Full experiment tracking with parameters, metrics, artifacts (feature importance plots, actual vs predicted scatter plots), and model registry
- **DVC:** Reproducible pipeline defined in `dvc.yaml` with three stages: generate_data → preprocess → train
- **Docker:** Multi-stage build (builder → runtime) with non-root user, health checks, and Docker Compose for local development stack (API + MLflow UI)

### 1.6 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict` | POST | ETA prediction with confidence intervals |
| `/health` | GET | Service health and model load status |
| `/docs` | GET | Interactive OpenAPI documentation |

### 1.7 Input Validation

Pydantic schemas enforce:
- GPS coordinate bounds (-90 to 90 lat, -180 to 180 lon)
- Cargo weight limits (0-20,000 kg; 100kg max for motorcycles)
- Time constraints (hour 0-23, day 0-6)
- Origin/destination must differ
- Automatic coordinate rounding to 6 decimal places

---

## 2. Medical RAG — Clinical Decision Support System

**GitHub Path:** `medical-rag/`  
**Repo Link:** https://github.com/blackcoderx/nGOT-sprints/tree/main/medical-rag

### 2.1 Problem Statement

Provide clinically-grounded answers to medical questions using Retrieval-Augmented Generation (RAG), with all answers citing source documents from medical guidelines.

### 2.2 Architecture

```
Client → FastAPI API → MedicalRAGEngine → LlamaIndex → Pinecone Vector Store
                                                    ↓
                                              OpenAI LLM (gpt-4o-mini)
                                                    ↓
                                          OpenAI Embeddings (text-embedding-3-small)
```

### 2.3 Technology Stack

| Component | Technology |
|-----------|-----------|
| API Framework | FastAPI 0.136+ |
| RAG Framework | LlamaIndex 0.14+ |
| Vector Database | Pinecone 6.0+ |
| Embeddings | OpenAI text-embedding-3-small |
| LLM | OpenAI gpt-4o-mini |
| Dependency Management | Poetry 2.0+ |
| Testing | Pytest 9.0+ |

### 2.4 Knowledge Base

Medical guideline documents ingested into Pinecone:
- Malaria treatment guidelines
- Hypertension management guidelines
- Diabetes management guidelines

### 2.5 Query Modes

**Direct Query (default):**
- Single retrieval + generation cycle
- Optimized for speed and simple questions
- Uses `similarity_top_k` for chunk retrieval

**Sub-Question Decomposition:**
- Breaks complex questions into sub-questions
- Retrieves independently for each sub-question
- Synthesizes final answer from multiple retrieval paths
- Example: "Compare malaria treatment to hypertension treatment targets" decomposes into separate queries for each condition

### 2.6 RAG Quality Controls

- **System Prompt:** Constrains LLM to answer ONLY from provided context
- **Citation Requirement:** Every answer must cite source guideline sections
- **Fallback Behavior:** Explicit "insufficient information" response when context lacks relevant data
- **Configurable Temperature:** 0.0 (deterministic) to 1.0 (creative), default 0.1

### 2.7 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ask` | POST | Clinical question with sourced answer |
| `/health` | GET | RAG engine status and vector count |
| `/sources` | GET | List all knowledge base documents |

### 2.8 Response Schema

Every response includes:
- Answer text grounded in guidelines
- Source documents with filename, chunk text, and relevance scores
- Number of sources used
- Query latency in milliseconds
- Model version information

---

## 3. Product Recommender — Semantic Search for E-Commerce

**GitHub Path:** `product-recommander/`  
**Repo Link:** https://github.com/blackcoderx/nGOT-sprints/tree/main/product-recommander

### 3.1 Problem Statement

Provide semantic product recommendations based on natural language queries (e.g., "something cozy to wear in the rain") using vector similarity search.

### 3.2 Architecture

```
Client → FastAPI API → ProductRecommender → OpenAI Embeddings
                                                    ↓
                                          Pinecone ANN Search
                                                    ↓
                                          Filtered + Ranked Results
```

### 3.3 Technology Stack

| Component | Technology |
|-----------|-----------|
| API Framework | FastAPI 0.136+ |
| Embeddings | OpenAI text-embedding-3-small |
| Vector Database | Pinecone 6.0+ / 8.1+ |
| Similarity | Cosine similarity via Pinecone ANN |
| Dependency Management | Poetry 2.0+ |
| Testing | Pytest 9.0+ + HTTPX |
| Code Quality | Black |

### 3.4 Recommendation Pipeline

1. **Embed:** Customer query text → 1536-dimensional vector via `text-embedding-3-small`
2. **Search:** Pinecone Approximate Nearest Neighbor (ANN) search for top-k matches
3. **Filter:** Optional metadata filtering by category and/or price range
4. **Rank:** Return results sorted by cosine similarity score

### 3.5 Filtering Strategy

- **Category Filter:** Exact match on product category metadata
- **Price Filter:** Less-than-or-equal comparison on price in Ghana Cedis
- **Over-fetching:** When filters are active, fetch 3× top_k to compensate for filtered-out results

### 3.6 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/recommend` | POST | Semantic product recommendations |
| `/health` | GET | Service health status |

### 3.7 Input Validation

- Query length: 3-500 characters
- Top-k: 1-10 recommendations
- Optional category and price filters with proper type constraints

---

## 4. Common Architectural Patterns

### 4.1 API Design

All three projects follow identical patterns:
- **FastAPI** as the web framework with automatic OpenAPI schema generation
- **CORSMiddleware** configured for cross-origin requests
- **Startup event** for lazy-loading of models/indexes
- **Health check endpoint** returning service status
- **Pydantic schemas** for rigorous input validation and output structuring
- **Error handling** with appropriate HTTP status codes (503 for unavailable services, 500 for internal errors)

### 4.2 Singleton Pattern

Each project uses a module-level singleton for its core engine:
- `ETAPredictor` — loads scikit-learn model once at startup
- `MedicalRAGEngine` — initializes LlamaIndex and Pinecone connection
- `ProductRecommender` — establishes OpenAI client and Pinecone index

### 4.3 Dependency Management

All projects use Poetry with:
- Production dependencies in `[project]` section
- Dev dependencies in `[dependency-groups].dev`
- Python version constraints (>=3.11)
- Pinned major versions with flexible minor/patch ranges

### 4.4 Testing

- **Pytest** as the test framework
- **HTTPX** for async API endpoint testing (where applicable)
- Test coverage across schemas, API endpoints, and core logic

---

## 5. Technical Decisions and Trade-offs

### 5.1 ETA Predictor

| Decision | Rationale |
|----------|-----------|
| Gradient Boosting over Deep Learning | Tabular data, interpretable, fast inference, no GPU needed |
| Synthetic data generation | No real logistics dataset available; enabled rapid prototyping |
| DVC for data versioning | Reproducible ML pipelines, track data-model lineage |
| Multi-stage Docker build | Smaller final image, no build tools in production |
| Non-root Docker user | Security best practice for containerized services |

### 5.2 Medical RAG

| Decision | Rationale |
|----------|-----------|
| LlamaIndex over LangChain | Simpler API for document ingestion and query engines |
| Pinecone over local vector store | Managed service, scalable, no infrastructure overhead |
| gpt-4o-mini over larger models | Cost-effective, sufficient quality for guideline-based QA |
| Sub-question query engine | Handles multi-hop clinical questions without custom orchestration |
| Low temperature (0.1) | Deterministic, factual responses required for clinical context |

### 5.3 Product Recommender

| Decision | Rationale |
|----------|-----------|
| Semantic search over collaborative filtering | No user interaction history; cold-start friendly |
| OpenAI embeddings over custom model | High-quality, zero-training, supports natural language |
| Pinecone metadata filtering | Single-query filtering without post-processing |
| Over-fetching strategy | Compensates for filter-induced result reduction |

---

## 6. Lessons Learned

1. **Input validation is critical:** Pydantic's field validators, model validators, and computed fields caught edge cases early (e.g., same origin/destination, motorcycle weight limits).

2. **Model versioning matters:** MLflow's experiment tracking made it easy to compare 5 different model configurations and select the best performer.

3. **RAG quality depends on prompts:** The system prompt in Medical RAG was the single most important factor in preventing hallucination and ensuring cited answers.

4. **Docker multi-stage builds reduce image size:** Separating build and runtime stages eliminated gcc, Poetry, and build dependencies from the final image.

5. **DVC pipelines ensure reproducibility:** The three-stage pipeline (generate → preprocess → train) made it trivial to re-run the entire ML workflow with a single command.

---

## 7. Future Work

### ETA Predictor
- Integrate real GPS routing APIs (Google Maps, OSRM) for actual road distances
- Add real-time traffic data as a feature
- Deploy model with proper CI/CD pipeline
- Implement prediction monitoring and drift detection

### Medical RAG
- Expand knowledge base to include more medical specialties
- Add document chunking strategies for longer guidelines
- Implement RAG evaluation metrics (faithfulness, answer relevance)
- Add user feedback loop for answer quality improvement

### Product Recommender
- Add collaborative filtering hybrid approach
- Implement A/B testing framework for recommendation quality
- Add personalization based on user history
- Support batch recommendation requests

---

## 8. Repository Structure

```
nGOT-sprints/
├── README.md
├── eta-predictor/
│   ├── app/                    # FastAPI application
│   ├── scripts/                # Data generation, preprocessing, training
│   ├── tests/                  # API and schema tests
│   ├── data/                   # Raw and processed data (DVC tracked)
│   ├── models/                 # Trained model artifacts
│   ├── metrics/                # Model evaluation metrics
│   ├── mlflow-artifacts/       # MLflow model artifacts
│   ├── dvc.yaml                # DVC pipeline definition
│   ├── Dockerfile              # Multi-stage Docker build
│   ├── docker-compose.yml      # Local development stack
│   └── pyproject.toml          # Poetry dependencies
├── medical-rag/
│   ├── app/                    # FastAPI application + RAG engine
│   ├── scripts/                # KB creation, ingestion, evaluation
│   ├── tests/                  # RAG engine tests
│   ├── data/                   # Source medical guidelines
│   ├── metrics/                # Evaluation metrics
│   ├── configs/                # Configuration files
│   └── pyproject.toml          # Poetry dependencies
└── product-recommander/
    ├── app/                    # FastAPI application + recommender
    ├── scripts/                # Catalogue creation, product indexing
    ├── tests/                  # Recommender tests
    ├── data/                   # Product catalogue data
    └── pyproject.toml          # Poetry dependencies
```

---

## 9. Conclusion

This 10-day sprint produced three production-grade AI/ML services, each demonstrating different aspects of modern AI engineering:

1. **Traditional ML with MLOps** (ETA Predictor) — scikit-learn, MLflow, DVC, Docker
2. **Retrieval-Augmented Generation** (Medical RAG) — LlamaIndex, Pinecone, OpenAI
3. **Semantic Search** (Product Recommender) — OpenAI embeddings, Pinecone ANN

All projects share a consistent API design, rigorous input validation, health monitoring, and test coverage. The common patterns across projects demonstrate a mature understanding of FastAPI architecture, Pydantic validation, and production-ready service design.

---

**GitHub Repository:** https://github.com/blackcoderx/nGOT-sprints  
**Submission Date:** May 16, 2026  
**Certification:** BUILD SCITECH 10-Day Sprint
