# Medical RAG

A FastAPI-based clinical decision support system that answers medical questions using Retrieval-Augmented Generation (RAG). All answers are grounded in medical guidelines and cite their sources.

## What This Project Does

- **Input**: Clinical questions (e.g., "What is the first-line treatment for malaria in Ghana?")
- **Output**: Answers with source citations, relevance scores, and latency metrics
- **Used by**: Healthcare applications and clinical decision support systems

## Tech Stack

- **API**: FastAPI
- **RAG Framework**: LlamaIndex
- **Vector Database**: Pinecone
- **Embeddings**: OpenAI `text-embedding-3-small`
- **LLM**: OpenAI `gpt-4o-mini`

## Project Structure

```
medical-rag/
├── app/
│   ├── main.py         # FastAPI application (API endpoints)
│   ├── rag_engine.py   # RAG engine with direct and sub-question query modes
│   └── schemas.py      # Request/response validation models
├── configs/            # Configuration files
├── scripts/
│   ├── create_knowledge_base.py  # Create the knowledge base documents
│   ├── ingest.py                 # Ingest documents into Pinecone
│   └── evaluate.py               # Evaluate RAG quality
├── data/               # Source medical guideline documents
├── metrics/            # Evaluation metrics
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
   PINECONE_INDEX_NAME=medical-literature
   ```

3. Ingest the knowledge base:
   ```bash
   poetry run python scripts/ingest.py
   ```

4. Run the API:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Open http://localhost:8000/docs for interactive API documentation.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ask` | POST | Ask a clinical question |
| `/health` | GET | Check RAG engine status and vector count |
| `/sources` | GET | List all documents in the knowledge base |

## Example Request

```json
{
  "question": "What is the first-line treatment for malaria in Ghana?",
  "top_k": 3,
  "use_sub_questions": false,
  "temperature": 0.1
}
```

## Query Modes

- **Direct query** (default): Single retrieval + generation. Fast and simple.
- **Sub-question decomposition**: Breaks complex questions into sub-questions, retrieves for each, then synthesizes. Slower but more accurate for multi-hop questions.

## Running Tests

```bash
poetry run pytest
```
