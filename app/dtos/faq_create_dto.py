from pydantic import BaseModel, Field, field_validator
from typing import Annotated

class FaqCreate(BaseModel):
    question: Annotated[str, Field(strict=True)]
    answer: Annotated[str, Field(strict=True)]

