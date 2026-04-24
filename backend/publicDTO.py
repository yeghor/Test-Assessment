from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List

from datetime import datetime


class ShortTravelProjects(BaseModel):
    project_id: str
    name: str
    description: str | None

class TravelProjectSchema(ShortTravelProjects):
    note: str

class TravelPlaceShort(BaseModel):
    place_id: str
    name: str
    visited: bool

class TravelPlace(TravelPlaceShort):
    note: str

class AccessibleProjectPlace(BaseModel):
    place_id: str
    place_name: str

# HTTP Bodies

class TravelProjectUpdate(BaseModel):
    name: str | None
    description: str | None

    start_date: datetime | None


class TravelProjectCreate(TravelProjectUpdate):
    name: str

    note: str = Field(default="")
    places: List[str]


class PlaceNote(BaseModel):
    place_id: str
    note: str


class Auth(BaseModel):
    username: str
    password: str
