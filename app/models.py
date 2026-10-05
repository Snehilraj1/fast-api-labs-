from sqlalchemy import Column, Float, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from .database import Base


class Patient(Base):
  __tablename__ = "patients"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(40), nullable=False)
  city = Column(String, nullable=False)
  age = Column(Integer, nullable=False)
  gender = Column(String, nullable=False)
  height = Column(Float, nullable=False)
  weight = Column(Float, nullable=False)
  bmi = Column(Float, nullable=False)
  verdict = Column(String, nullable=False)
  added_at = Column(
      TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
  )