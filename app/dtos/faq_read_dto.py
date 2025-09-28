from pydantic import BaseModel, Field
from typing import Annotated

class FaqRead(BaseModel):
    id: Annotated[int, Field(strict=True)]
    question: Annotated[str, Field(min_length=1, max_length=500)]
    answer: Annotated[str, Field(min_length=1)]


