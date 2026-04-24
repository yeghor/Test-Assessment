from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List

from datetime import datetime


class TravelProjectSchema(BaseModel):
    project_id: str
    name: str
    description: str | None
    start_date: str  # Datetime compatible string


class TravelPlaceShort(BaseModel):
    place_id: str
    place_name: str
    visited: bool


class TravelPlaceSchema(TravelPlaceShort):
    note: str


class AccessibleProjectPlace(BaseModel):
    place_id: str
    place_name: str


# HTTP Bodies


class TravelProjectUpdate(BaseModel):
    name: str | None
    description: str | None

    start_date: datetime | None


class TravelPlaceUpdate(BaseModel):
    visited: bool | None
    note: str | None


class TravelProjectCreate(TravelProjectUpdate):
    name: str

    places: List[str]


class PlaceNote(BaseModel):
    place_id: str
    note: str


class Auth(BaseModel):
    username: str
    password: str
