from pydantic import BaseModel, Field, WithJsonSchema, field_validator
from typing import Annotated

class FaqRead(BaseModel):
    id: Annotated[int, Field(strict=True), WithJsonSchema()]
    question: Annotated[str, Field(min_length=1, max_length=500), WithJsonSchema()]
    answer: Annotated[str, Field(min_length=1), WithJsonSchema()]


