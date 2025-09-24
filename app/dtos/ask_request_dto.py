from pydantic import BaseModel, Field
from typing import Annotated

class AskRequest(BaseModel):
    question: Annotated[str, Field(strict=True)]

    