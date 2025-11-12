"""Pydantic models for CV Optimizer state management."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewFeedback(BaseModel):
    """Model for reviewer feedback."""

    iteration: int = Field(..., description="Iteration number")
    decision: str = Field(..., description="APPROVE or REVISE")
    comments: str = Field(..., description="Detailed feedback comments")
    improvements_needed: list[str] = Field(
        default_factory=list, description="List of specific improvements"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Timestamp of feedback"
    )


class CVOptimizerState(BaseModel):
    """State model for CV optimization flow."""

    # Inputs
    job_description: str = Field("", description="Job description text")
    cv_draft: str = Field("", description="Original CV draft")
    supporting_docs: list[str] = Field(
        default_factory=list, description="Additional supporting documents"
    )

    # Processing
    current_cv: str = Field("", description="Current version of CV being processed")
    iteration_count: int = Field(0, description="Current iteration number")
    max_iterations: int = Field(3, description="Maximum number of iterations")

    # Feedback tracking
    feedback_history: list[ReviewFeedback] = Field(
        default_factory=list, description="History of all reviewer feedback"
    )

    # Status
    status: str = Field("INITIALIZED", description="Current flow status")
    final_decision: str | None = Field(None, description="Final decision from reviewer")

    model_config = ConfigDict(arbitrary_types_allowed=True)
