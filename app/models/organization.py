from sqlalchemy import Column, String, Integer, ForeignKey, Table, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("organization_id", Integer, ForeignKey("organizations.id")),
    Column("activity_id", Integer, ForeignKey("activities.id")),
    Column("is_primary", Boolean, default=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now())
)

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    description = Column(String)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    building = relationship("Building", back_populates="organizations")
    activities = relationship("Activity", secondary=organization_activities)