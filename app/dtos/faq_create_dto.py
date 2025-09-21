from pydantic import BaseModel, Field, WithJsonSchema, field_validator
from typing import Annotated

class FaqCreate(BaseModel):
    question: Annotated[str, Field(strict=True), WithJsonSchema()]
    answer: Annotated[str, Field(strict=True), WithJsonSchema()]

