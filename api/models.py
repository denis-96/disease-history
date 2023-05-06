from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from config import ASYNC_DB_URL

engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)

    patients = relationship("Patient", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"User(id={self.id}, email={self.email})"


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    full_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False, default=0)
    diagnosis = Column(String)
    complaints = Column(String)
    anamnesis = Column(String)
    heredity = Column(String)
    treatment_comments = Column(String)

    treatment_records = relationship(
        "TreatmentRecord", backref="patient", lazy="dynamic"
    )


class TreatmentRecord(Base):
    __tablename__ = "treatment_records"
    id = Column(Integer, primary_key=True)
    patient_id = Column(
        Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)

    rubrics = relationship("RubricVariant", backref="record", lazy="dynamic")


class RubricSection(Base):
    __tablename__ = "rubric_sections"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    rubrics = relationship("Rubric", backref="section", lazy="dynamic")


class Rubric(Base):
    __tablename__ = "rubrics"
    id = Column(Integer, primary_key=True)
    section_id = Column(
        Integer, ForeignKey("rubric_sections.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String, nullable=False)


class RubricVariant(Base):
    __tablename__ = "rubrics_variants"
    id = Column(Integer, primary_key=True)
    rubric_id = Column(
        Integer, ForeignKey("rubrics.id", ondelete="CASCADE"), nullable=False
    )
    record_id = Column(
        Integer, ForeignKey("treatment_records.id", ondelete="CASCADE"), nullable=False
    )
    description = Column(String, nullable=False)

    rubric = relationship("Rubric")
