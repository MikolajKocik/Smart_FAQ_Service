from pydantic import BaseModel, Field, WithJsonSchema
from typing import Annotated

class AskRequest(BaseModel):
    question: Annotated[str, Field(strict=True), WithJsonSchema()]

    