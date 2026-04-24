from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base, TravelPlace, TravelProject


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

    async def get_projects(self) -> List[TravelProject]:
        result = await self._session.execute(select(TravelProject))
        return result.scalars().all()

    async def get_project(self, project_id: str) -> Optional[TravelProject]:
        result = await self._session.execute(
            select(TravelProject).where(TravelProject.project_id == project_id)
        )
        return result.scalar_one_or_none()

    async def get_project_places(
        self, project_id: str
    ) -> List[TravelPlace]:
        result = await self._session.execute(
            select(TravelPlace).where(TravelPlace.project_id == project_id)
        )
        return result.scalars().all()

    async def get_project_place(
        self, project_id: str, place_id: str
    ) -> Optional[TravelPlace]:
        result = await self._session.execute(
            select(TravelPlace).where(
                TravelPlace.project_id == project_id,
                TravelPlace.place_id == place_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_visited_places(self, project_id: str) -> List[TravelPlace]:
        result = await self._session.execute(
            select(TravelPlace).where(
                TravelPlace.project_id == project_id,
                TravelPlace.visited == True,
            )
        )
        return result.scalars().all()

    async def delete_places_by_project(self, project_id: str) -> None:
        await self._session.execute(
            delete(TravelPlace).where(TravelPlace.project_id == project_id)
        )
        await self._session.flush()
