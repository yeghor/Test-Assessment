from sqlalchemy.ext.asyncio import AsyncSession

from database import TravelPlace, TravelPlaceNote, TravelProject, Base

class PostgresService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, instance: Base) -> None:
        self._session.add(instance)

    async def delete(self, instance: Base) -> None:
        self._session.delete(instance)
        await self._session.flush()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def close(self) -> None:
        await self._session.close()

    async def get_projects(self, user_id: str) -> TravelProject:
        pass

    async def get_project_places(self, user_id: str, project_id: str) -> TravelPlace:
        pass
