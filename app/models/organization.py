from sqlalchemy import Column, String, Integer, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from core.database import Base

organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id"), primary_key=True),
    Column("is_primary", Boolean, default=False) 
)

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    placement = relationship(
        "Building",
        back_populates="address",
        cascade="all, delete-orphan"
    )
    activities = relationship(
        "Activity",
        secondary="organization_activities",
        cascade="all, delete-orphan"
    )