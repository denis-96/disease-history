from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from ..database import Base


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
