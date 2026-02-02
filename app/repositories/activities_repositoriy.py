from models.activities import Activity
from sqlalchemy.ext.asyncio import AsyncSession


class ActivitiesRepository:

    def create(self, db:AsyncSession, activity:Activity):
        db.add(activity)
        return activity