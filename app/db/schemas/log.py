from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from .common.Base import Base
from typing import Optional

class Log(Base):
    __tablename__="logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    log_info: Mapped[Optional[str]] = mapped_column(Text)
    log_critical: Mapped[Optional[str]] = mapped_column(Text)
    log_warning: Mapped[Optional[str]] = mapped_column(Text)