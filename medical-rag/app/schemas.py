from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MedicalQuery(BaseModel):
    """Input schema for the /ask endpoint."""

    model_config = ConfigDict(extra="forbid")

    question: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Clinical question to answer",
        examples=["What is the first-line treatment for malaria in Ghana?"],
    )
    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of source documents to retrieve",
    )
    use_sub_questions: bool = Field(
        default=False,
        description="Use multi-step query decomposition for complex questions",
    )
    temperature: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        description="LLM temperature (0=deterministic, 1=creative)",
    )


class SourceDocument(BaseModel):
    """A retrieved source document used to generate the answer."""

    filename: str
    chunk_text: str
    relevance_score: float


class MedicalAnswer(BaseModel):
    """Output schema for the /ask endpoint."""

    answer: str
    sources: list[SourceDocument]
    question: str
    num_sources_used: int
    latency_ms: float
    model_used: str
    answer_timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    status: Literal["healthy", "degraded"]
    index_loaded: bool
    vector_count: int
