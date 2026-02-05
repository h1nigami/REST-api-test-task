from sqlalchemy import Column, String, Integer, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

# Ассоциативная таблица для связи многие-ко-многим
organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("organization_id", Integer, ForeignKey("organizations.id")),
    Column("activity_id", Integer, ForeignKey("activities.id")),
    Column("is_primary", Boolean, default=False)
)

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    description = Column(String)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    
    building = relationship("Building", back_populates="organizations")
    activities = relationship("Activity", secondary=organization_activities)