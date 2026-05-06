# Product Recommender

A FastAPI-based semantic product recommendation service powered by vector similarity search. Supports natural language queries like "something cozy to wear in the rain".

## What This Project Does

- **Input**: Customer query with optional category and price filters
- **Output**: Ranked product recommendations with similarity scores
- **Used by**: E-commerce applications and storefronts

## Tech Stack

- **API**: FastAPI
- **Embeddings**: OpenAI `text-embedding-3-small`
- **Vector Database**: Pinecone
- **Similarity**: Cosine similarity via Pinecone ANN search

## Project Structure

```
product-recommander/
├── app/
│   ├── main.py        # FastAPI application (API endpoints)
│   ├── recommender.py # Product recommendation engine
│   └── schemas.py     # Request/response validation models
├── scripts/
│   ├── create_catalogue.py    # Create product catalogue data
│   └── index_products.py      # Embed and index products into Pinecone
├── data/               # Product data
└── tests/              # Test suite
```

## Quick Start

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Set up environment variables (`.env`):
   ```
   OPENAI_API_KEY=your-key
   PINECONE_API_KEY=your-key
   ```

3. Index products:
   ```bash
   poetry run python scripts/index_products.py
   ```

4. Run the API:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Open http://localhost:8000/docs for interactive API documentation.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/recommend` | POST | Get product recommendations |
| `/health` | GET | Check service status |

## Example Request

```json
{
  "query": "something cozy to wear in the rain",
  "top_k": 5,
  "category_filter": "Fashion",
  "max_price_ghs": 150.0
}
```

## Recommendation Pipeline

1. **Embed** the customer query using `text-embedding-3-small`
2. **Search** Pinecone for top-k nearest neighbors
3. **Filter** by optional category and price constraints
4. **Return** ranked recommendations with similarity scores

## Running Tests

```bash
poetry run pytest
```
