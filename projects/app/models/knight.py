from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Knight(Base):
    __tablename__ = "knights"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    sword_name: Mapped[str | None] = mapped_column(default=None)
    is_kingsguard: Mapped[bool] = mapped_column(default=False)
