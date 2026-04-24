from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from publicDTO import *
from services.domain import TravelingService

traveling = APIRouter()


@traveling.post("/", summary="Create a travel project")
async def create_travel_project(
    travel_object: TravelProjectCreate, session: AsyncSession
) -> None:
    """Create a travel project with optional imported places."""

    traveling_service = TravelingService(session=session)

    try:
        await traveling_service.create_project()
        await traveling_service.commit_changes()
    except HTTPException:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@traveling.get("/", summary="List travel projects")
async def list_travel_projects(session: AsyncSession) -> List[ShortTravelProjects]:
    """List all travel projects."""

    traveling_service = TravelingService(session=session)

    try:
        await traveling_service.list_projects()
        await traveling_service.commit_changes()
    except HTTPException:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@traveling.get("/{project_id}", summary="Get a single travel project")
async def get_travel_project(
    project_id: str, session: AsyncSession
) -> TravelProjectSchema:
    """Get travel project details by project_id."""

    traveling_service = TravelingService(session=session)


@traveling.put("/{project_id}", summary="Update a travel project")
async def update_travel_project(
    project_id: str, travel_project: TravelProjectUpdate, session: AsyncSession
) -> None:
    """Update travel project name, description, or start date."""

    traveling_service = TravelingService(session=session)

    try:
        await traveling_service.update_project()
        await traveling_service.commit_changes()
    except HTTPException:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@traveling.delete("/{project_id}", summary="Delete a travel project")
async def delete_travel_project(project_id: str, session: AsyncSession) -> None:
    """Delete a travel project if no places are marked as visited"""

    traveling_service = TravelingService(session=session)

    try:
        await traveling_service.delete_travel_project()
        await traveling_service.commit_changes()
    except HTTPException:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@traveling.post("/{project_id}/places", summary="Add a place to a travel project")
async def add_place_to_project(
    project_id: str, place_name: str, session: AsyncSession
) -> None:
    """Add a place to an existing project after validating the external place ID."""

    traveling_service = TravelingService(session=session)

    try:
        await traveling_service.add_project_place()
        await traveling_service.commit_changes()
    except HTTPException:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@traveling.patch("/{project_id}/places/{place_id}", summary="Update a project place")
async def update_place_in_project(
    project_id: str, place_id: str, visited: bool, session: AsyncSession
) -> None:
    """Update notes or visited state for a place in a project."""

    traveling_service = TravelingService(session=session)

    try:
        await traveling_service.update_project_place()
        await traveling_service.commit_changes()
    except HTTPException:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@traveling.get("/{project_id}/places", summary="List all places for a travel project")
async def list_project_places(
    project_id: str, session: AsyncSession
) -> List[TravelPlaceShort]:
    """List all places associated with a travel project."""

    traveling_service = TravelingService(session=session)

    try:
        await traveling_service.list_project_places()
        await traveling_service.commit_changes()
    except HTTPException:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@traveling.get(
    "/{project_id}/places/{place_id}",
    summary="Get a single place within a travel project",
)
async def get_project_place(
    project_id: str, place_id: str, session: AsyncSession
) -> TravelPlace:
    """Get details for a single place within a project"""

    traveling_service = TravelingService(session=session)

    try:
        await traveling_service.get_project_place()
        await traveling_service.commit_changes()
    except HTTPException:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
