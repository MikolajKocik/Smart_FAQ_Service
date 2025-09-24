from pydantic import BaseModel, Field
from typing import Annotated

class AskResponse(BaseModel):
    answer: Annotated[str, Field(strict=True)]