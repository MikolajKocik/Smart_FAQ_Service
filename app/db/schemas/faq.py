from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from .common.Base import Base

class FAQ(Base):
    __tablename__ = "faqs"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(Text())
    answer: Mapped[str] = mapped_column(Text())
