from pydantic import BaseModel, Field, WithJsonSchema
from typing import Annotated

class AskResponse(BaseModel):
    answer: Annotated[str, Field(strict=True), WithJsonSchema()]