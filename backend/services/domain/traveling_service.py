from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from services.repository import PostgresService, PlacesAPI

from publicDTO import *
from database import TravelProject, TravelPlace

from uuid import uuid4

import asyncio

from config import settings


class TravelingService:
    def __init__(self, session: AsyncSession):
        self._postgres_service = PostgresService(session)
        self._places_api = PlacesAPI()

    async def commit_changes(self) -> None:
        """Must be always called to keep all changes"""
        await self._postgres_service.commit()

    async def create_project(self, project: TravelProjectCreate) -> None:
        if not 1 <= len(project.places) <= 10:
            raise HTTPException(
                status_code=400,
                detail="Number of places must be at least 1 and less than 10",
            )

        # Duplicate places check
        # https://stackoverflow.com/questions/5278122/checking-if-all-elements-in-a-list-are-unique
        if len(project.places) != len(set(project.places)):
            raise HTTPException(
                status_code=400, detail="Project must contain unique places"
            )

        place_names = await asyncio.gather(
            *[
                self._places_api.check_place(place_id=place_id)
                for place_id in project.places
            ]
        )

        for i, place_name in enumerate(place_names):
            if place_name is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Place {project.places[i]} does not exist",
                )

        project_id = str(uuid4())
        travel_project = TravelProject(
            project_id=project_id,
            name=project.name,
            description=project.description,
            start_date=project.start_date,
        )

        await self._postgres_service.add(travel_project)

        for place_id, place_name in zip(project.places, place_names):
            await self._postgres_service.add(
                TravelPlace(
                    place_id=place_id,
                    project_id=project_id,
                    place_name=place_name,
                )
            )

    async def update_project(
        self, project_id: str, project: TravelProjectUpdate
    ) -> None:
        db_project = await self._postgres_service.get_project(project_id)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        if project.name is not None:
            db_project.name = project.name
        if project.description is not None:
            db_project.description = project.description
        if project.start_date is not None:
            db_project.start_date = project.start_date

    async def delete_project(self, project_id: str) -> None:
        db_project = await self._postgres_service.get_project(project_id)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        visited_places = await self._postgres_service.get_visited_places(project_id)
        if visited_places:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete a project with visited places",
            )

        project_places = await self._postgres_service.get_project_places("", project_id)
        for place in project_places:
            await self._postgres_service.delete(place)

        await self._postgres_service.delete(db_project)

    async def add_project_place(self, place_id: str, project_id: str) -> None:
        db_project = await self._postgres_service.get_project(project_id)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        existing_place = await self._postgres_service.get_project_place(
            project_id, place_id
        )
        if existing_place is not None:
            raise HTTPException(
                status_code=400,
                detail="Place already added to this project",
            )

        place_name = await self._places_api.check_place(place_id=place_id)
        if place_name is None:
            raise HTTPException(status_code=404, detail="Place does not exist")

        await self._postgres_service.add(
            TravelPlaceSchema(
                place_id=place_id,
                project_id=project_id,
                place_name=place_name,
            )
        )

    async def delete_project_place(self, place_id: str, project_id: str) -> None:
        db_place = await self._postgres_service.get_project_place(project_id, place_id)
        if db_place is None:
            raise HTTPException(status_code=404, detail="Place not found")

        await self._postgres_service.delete(db_place)

    async def get_projects(self) -> List[TravelProjectSchema]:
        projects = await self._postgres_service.get_projects()
        return [
            TravelProjectSchema(
                project_id=project.project_id,
                name=project.name,
                description=project.description,
                start_date=project.start_date.strftime(format=settings.datetime_format),
            )
            for project in projects
        ]

    async def get_project(self, project_id: str) -> TravelProjectSchema:
        db_project = await self._postgres_service.get_project(project_id)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        return TravelProjectSchema(
            project_id=db_project.project_id,
            name=db_project.name,
            description=db_project.description,
            start_date=db_project.start_date.strftime(settings.datetime_format),
        )

    async def search_places(self, query: str) -> List[AccessibleProjectPlace]:
        remote_places = await self._places_api.search_places(query)
        return [
            AccessibleProjectPlace(
                place_id=place["place_id"],
                place_name=place["name"],
            )
            for place in remote_places
        ]

    async def get_project_place(
        self, project_id: str, place_id: str
    ) -> TravelPlaceSchema:
        db_place = await self._postgres_service.get_project_place(project_id, place_id)
        if db_place is None:
            raise HTTPException(status_code=404, detail="Place not found")

        return TravelPlaceSchema(
            place_id=db_place.place_id,
            place_name=db_place.place_name,
            visited=db_place.visited,
            note=db_place.note,
        )

    async def update_project_place(
        self, project_id: str, place_id: str, data: TravelPlaceUpdate
    ) -> None:
        db_place = await self._postgres_service.get_project_place(project_id, place_id)
        if db_place is None:
            raise HTTPException(status_code=404, detail="Place not found")

        if data.visited:
            db_place.visited = data.visited
        if data.note is not None:
            print(data.note)
            db_place.note = data.note
            print(db_place.note)

    async def get_project_places(self, project_id: str) -> List[TravelPlaceShort]:
        project_places = await self._postgres_service.get_project_places(project_id)
        return [
            TravelPlaceShort(
                place_id=place.place_id,
                place_name=place.place_name,
                visited=place.visited,
            )
            for place in project_places
        ]

    async def get_possible_project_places(
        self, page: int
    ) -> List[AccessibleProjectPlace]:
        project_places = await self._places_api.get_places(page=page)
        return [
            AccessibleProjectPlace(place_id=place["place_id"], place_name=place["name"])
            for place in project_places
        ]
