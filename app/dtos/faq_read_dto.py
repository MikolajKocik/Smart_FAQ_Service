from pydantic import BaseModel, Field, WithJsonSchema, field_validator
from typing import Annotated

class FaqRead(BaseModel):
    id: Annotated[int, Field(strict=True), WithJsonSchema()]
    question: Annotated[str, Field(strict=True), WithJsonSchema()]
    answer: Annotated[str, Field(strict=True), WithJsonSchema()]
 
    #@field_validator zrobic dla dto