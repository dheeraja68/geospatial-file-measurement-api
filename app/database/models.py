from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from datetime import datetime

from app.database.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    feature_count = Column(Integer, default=0)
    original_crs = Column(String, nullable=True)
    measurement_crs = Column(String, nullable=True)
    status = Column(String, default="PROCESSING")
    created_at = Column(DateTime, default=datetime.utcnow)


class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)

    feature_index = Column(Integer, nullable=False)
    geometry_type = Column(String, nullable=False)
    geometry = Column(Text, nullable=True)
    properties = Column(Text, nullable=True)

    area_sq_m = Column(Float, nullable=True)
    length_m = Column(Float, nullable=True)