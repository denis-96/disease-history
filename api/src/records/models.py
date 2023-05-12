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

    patient: Mapped["Patient"] = relationship(back_populates="treatment_records")
    rubrics: Mapped[List["RubricVariant"]] = relationship(
        back_populates="record", cascade="all, delete-orphan", lazy="joined"
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
    rubric: Mapped["Rubric"] = relationship("Rubric")

    def __repr__(self):
        return f"RubricVariant(id={self.id}, rubric={self.rubric}, description={self.description})"


class RubricSection(Base):
    __tablename__ = "rubric_sections"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    rubrics: Mapped[List["Rubric"]] = relationship(
        back_populates="section", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"RubricSection(id={self.id}, title={self.title})"


class Rubric(Base):
    __tablename__ = "rubrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    section_id: Mapped[int] = mapped_column(
        ForeignKey("rubric_sections.id", ondelete="CASCADE")
    )
    title: Mapped[str]

    section: Mapped["RubricSection"] = relationship(back_populates="rubrics")

    def __repr__(self):
        return f"Rubric(id={self.id}, title={self.title})"


from ..patients.models import Patient
