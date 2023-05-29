from typing import List, Optional

from sqlalchemy import ForeignKey, asc
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[Optional[str]]
    age: Mapped[int] = mapped_column(default=0)
    diagnosis: Mapped[Optional[str]]
    complaints: Mapped[Optional[str]]
    anamnesis: Mapped[Optional[str]]
    heredity: Mapped[Optional[str]]
    treatment_plan: Mapped[Optional[str]]
    treatment_comments: Mapped[Optional[str]]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="patients")
    treatment_records: Mapped[List["TreatmentRecord"]] = relationship(
        back_populates="patient",
        cascade="all, delete-orphan",
        order_by=lambda: asc(TreatmentRecord.date),
    )

    def __repr__(self):
        return f"Patient(id={self.id}, full_name={self.full_name})"


from ..models import User
from ..records.models import TreatmentRecord
