from fastapi import HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from publicDTO import *
from services.domain import TravelingService

from database import get_session_depends

traveling = APIRouter()


@traveling.post("/", summary="Create a travel project")
async def create_travel_project(
    travel_object: TravelProjectCreate,
    session: AsyncSession = Depends(get_session_depends),
) -> None:
    """Create a travel project with optional imported places."""

    traveling_service = TravelingService(session=session)

    try:
        await traveling_service.create_project(travel_object)
        await traveling_service.commit_changes()
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@traveling.get("/", summary="List travel projects")
async def list_travel_projects(
    session: AsyncSession = Depends(get_session_depends),
) -> List[TravelProjectSchema]:
    """List all travel projects."""

    traveling_service = TravelingService(session=session)

    try:
        return await traveling_service.get_projects()
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@traveling.get("/{project_id}", summary="Get a single travel project")
async def get_travel_project(
    project_id: str, session: AsyncSession = Depends(get_session_depends)
) -> TravelProjectSchema:
    """Get travel project details by project_id."""

    traveling_service = TravelingService(session=session)

    try:
        return await traveling_service.get_project(project_id)
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@traveling.put("/{project_id}", summary="Update a travel project")
async def update_travel_project(
    project_id: str,
    travel_project: TravelProjectUpdate,
    session: AsyncSession = Depends(get_session_depends),
) -> None:
    """Update travel project name, description, or start date."""

    traveling_service = TravelingService(session=session)

    try:
        await traveling_service.update_project(project_id, travel_project)
        await traveling_service.commit_changes()
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@traveling.delete("/{project_id}", summary="Delete a travel project")
async def delete_travel_project(
    project_id: str, session: AsyncSession = Depends(get_session_depends)
) -> None:
    """Delete a travel project if no places are marked as visited"""

    traveling_service = TravelingService(session=session)

    try:
        await traveling_service.delete_project(project_id)
        await traveling_service.commit_changes()
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@traveling.post("/{project_id}/places", summary="Add a place to a travel project")
async def add_place_to_project(
    project_id: str, place_id: str, session: AsyncSession = Depends(get_session_depends)
) -> None:
    """Add a place to an existing project after validating the external place ID."""

    traveling_service = TravelingService(session=session)

    try:
        await traveling_service.add_project_place(place_id, project_id)
        await traveling_service.commit_changes()
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@traveling.patch("/{project_id}/places/{place_id}", summary="Update a project place")
async def update_place_in_project(
    project_id: str,
    place_id: str,
    data: TravelPlaceUpdate,
    session: AsyncSession = Depends(get_session_depends),
) -> None:
    """Update notes or visited state for a place in a project."""

    traveling_service = TravelingService(session=session)

    try:
        await traveling_service.update_project_place(project_id, place_id, data)
        await traveling_service.commit_changes()
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@traveling.get("/{project_id}/places", summary="List all places for a travel project")
async def get_project_places(
    project_id: str, session: AsyncSession = Depends(get_session_depends)
) -> List[TravelPlaceShort]:
    """List all places associated with a travel project."""

    traveling_service = TravelingService(session=session)

    try:
        return await traveling_service.get_project_places(project_id)
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@traveling.get(
    "/{project_id}/places/{place_id}",
    summary="Get a single place within a travel project",
)
async def get_project_place(
    project_id: str, place_id: str, session: AsyncSession = Depends(get_session_depends)
) -> TravelPlaceSchema:
    """Get details for a single place within a project"""

    traveling_service = TravelingService(session=session)

    try:
        return await traveling_service.get_project_place(project_id, place_id)
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@traveling.get(
    "/places/allowed/{page}",
    summary="Get possible places for a project",
)
async def get_allowed_project_places(
    page: int, session: AsyncSession = Depends(get_session_depends)
) -> List[AccessibleProjectPlace]:
    """Get details for a single place within a project"""

    traveling_service = TravelingService(session=session)

    try:
        return await traveling_service.get_possible_project_places(page)
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@traveling.get(
    "/places/allowed",
    summary="Search possible places for a project",
)
async def search_allowed_project_places(
    query: str, session: AsyncSession = Depends(get_session_depends)
) -> List[AccessibleProjectPlace]:
    """Search possible places for a project"""

    if not query:
        query = ""

    traveling_service = TravelingService(session=session)

    try:
        return await traveling_service.search_places(query=query)
    except HTTPException as e:
        raise e from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
