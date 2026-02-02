from models.organization import Organization
from sqlalchemy.ext.asyncio import AsyncSession


class OrganizationsRepository:

    def create(self, db:AsyncSession, organization:Organization):
        db.add(organization)
        return organization