from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint, asc, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class TreatmentRecord(Base):
    __tablename__ = "treatment_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    date: Mapped[datetime] = mapped_column(insert_default=func.now())

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE")
    )

    patient: Mapped["Patient"] = relationship(back_populates="treatment_records")
    rubrics: Mapped[List["RubricVariant"]] = relationship(
        back_populates="record",
        cascade="all, delete-orphan",
        lazy="joined",
        order_by=lambda: asc(RubricVariant.rubric_id),
    )

    def __repr__(self):
        return f"TreatmentRecord(id={self.id}, title={self.title}, date={self.date.date()})"


class RubricVariant(Base):
    __tablename__ = "rubrics_variants"
    id: Mapped[int] = mapped_column(primary_key=True)
    rubric_id: Mapped[int] = mapped_column(
        ForeignKey("rubrics.id", ondelete="SET NULL")
    )
    record_id: Mapped[int] = mapped_column(
        ForeignKey("treatment_records.id", ondelete="CASCADE")
    )
    description: Mapped[str]

    record: Mapped["TreatmentRecord"] = relationship(back_populates="rubrics")
    rubric: Mapped["Rubric"] = relationship("Rubric", lazy="joined")

    __table_args__ = (UniqueConstraint("rubric_id", "record_id", name="rub_id_rec_id"),)

    def __repr__(self):
        return f"RubricVariant(id={self.id}, rubric={self.rubric}, description={self.description})"


from ..patients.models import Patient
from ..rubrics.models import Rubric
