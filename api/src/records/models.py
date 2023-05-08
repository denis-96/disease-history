from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

from ..database import Base


class TreatmentRecord(Base):
    __tablename__ = "treatment_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    date: Mapped[datetime] = mapped_column(insert_default=func.now())

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE")
    )

    patient: Mapped["Patient"] = relationship(
        back_populates="treatment_records", lazy="dynamic"
    )
    rubrics: Mapped[List["RubricVariant"]] = relationship(
        back_populates="record", lazy="dynamic"
    )

    def __repr__(self):
        return f"TreatmentRecord(id={self.id}, title={self.title}, date={self.date.date()})"


class RubricVariant(Base):
    __tablename__ = "rubrics_variants"
    id: Mapped[int] = mapped_column(primary_key=True)
    rubric_id: Mapped[int] = mapped_column(ForeignKey("rubrics.id", ondelete="CASCADE"))
    record_id: Mapped[int] = mapped_column(
        ForeignKey("treatment_records.id", ondelete="CASCADE")
    )
    description: Mapped[str]

    record: Mapped["TreatmentRecord"] = relationship(
        back_populates="rubrics", lazy="dynamic"
    )
    rubric: Mapped["Rubric"] = relationship("Rubric")

    def __repr__(self):
        return f"RubricVariant(id={self.id}, rubric={self.rubric}, description={self.description})"


from ..models import Rubric
from ..patients.models import Patient
