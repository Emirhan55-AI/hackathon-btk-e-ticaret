from pydantic import BaseModel, Field
from typing import List, Dict, Any
import uuid

class QuizQuestion(BaseModel):
    """Model for a quiz question."""
    question_id: str
    question_text: str
    options: List[str]

class QuizAnswer(BaseModel):
    """Model for a single quiz answer."""
    question_id: str
    selected_option: str
    option_value: Any = None  # For storing numeric/categorical values

class QuizResponse(BaseModel):
    """Model for a user's complete quiz response."""
    answers: List[QuizAnswer] = Field(..., min_items=1)
