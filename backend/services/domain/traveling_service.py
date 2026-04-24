from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from services.repository import PostgresService, PlacesAPI

from publicDTO import *
from database import TravelProject, TravelPlace

from uuid import uuid4

import asyncio


class TravelingService:
    def __init__(self, session: AsyncSession):
        self._postgres_service = PostgresService(session)
        self._places_api = PlacesAPI(session)

    def commit_changes(commit: bool):
        """Must be always called to keep all changes"""

    async def create_project(self, project: TravelProjectCreate) -> None:
        if not 1 <= len(project.places) <= 10:
            raise HTTPException(
                status_code=400,
                detail="Number of places must be at least 1 and less than 10",
            )

        places_validation_result = asyncio.gather(
            *[
                lambda: self._places_api.check_place(place_id=place_id)
                for place_id in project.places
            ]
        )

        for i, place_name in enumerate(places_validation_result):
            if place_name is None:
                raise HTTPException(f"Place {project.places[i]} does not exist")

        project_id = str(uuid4())

        for i, place_name in enumerate(places_validation_result):
            await self._postgres_service.add(
                TravelPlace(
                    place_id=project.places[i],
                    project_id=project_id,
                    place_name=place_name,
                )
            )

        await self._postgres_service.add(
            TravelProject(
                project_id=project_id,
                name=project.name,
                description=project.description,
                start_date=project.start_date,
                note=project.note,
            )
        )

    def update_project(self, project: TravelProjectUpdate) -> None:
        pass

    def delete_project(self, project_id: str) -> None:
        pass

    def add_project_place(self, place_id: str, project_id: str) -> None:
        pass

    def delete_project_place(self, place_id: str, project_id: str) -> None:
        pass

    def list_projects(self) -> List[ShortTravelProjects]:
        pass

    def get_project(self, project_id: str) -> TravelProjectSchema:
        pass

    def get_project_places(self) -> List[TravelPlaceShort]:
        pass

    async def search_places(self) -> List[AccessibleProjectPlace]:
        pass

    async def list_project_places(self) -> List[TravelPlace]:
        pass
