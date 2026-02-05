from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.core.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    
    parent = relationship(
        "Activity",
        remote_side=[id],
        backref=backref("children", cascade="all, delete-orphan"),
        lazy="joined"
    )

    def __repr__(self):
        return f"<Activity(id={self.id}, name={self.name})>"
    
    @property
    def level(self):
        if not self.parent_id:
            return 0
        return self.parent.level + 1 if self.parent else 1
    
    def get_full_path(self, separator=" > "):
        if self.parent:
            return f"{self.parent.get_full_path(separator)}{separator}{self.name}"
        return self.name