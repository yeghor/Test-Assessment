from fastapi import HTTPException

from typing import List, Any, TypedDict
import aiohttp


class PlaceDict(TypedDict):
    name: str
    place_id: str

class PlacesAPI:
    def __init__(self):
        self._base_url = "https://api.artic.edu/api/v1/places"

    @staticmethod
    def _validate_failed_request(status_code: int, skip_404: bool = False) -> None:
        """Raises a HTTPException on failed request"""

        if status_code != 200 or (status_code == 404 and not skip_404):
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    def _map_places(raw_api_data: any) -> List[PlaceDict]:
        out = []
        for data in raw_api_data["data"]:
            out.append(
                {
                    "name": data["title"],
                    "place_id": str(data["id"])
                }
            )
        return out

    async def check_place(self, place_id: str) -> str:
        """Returns names of the places, if name None, this place does not exist"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._base_url}/{place_id}") as response:
                self._validate_failed_request(response.status, skip_404=True)                
                
                if response.status == 404:
                    return None
                
                data = await response.json()
                return data["data"]["id"]

    async def get_places(self, page: int) -> List[PlaceDict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._base_url}?page={page}&limit={50}") as response:
                self._validate_failed_request(response.status)                
                data = await response.json()
                return self._map_places(data)

    async def search_places(self, query: str) -> List[PlaceDict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._base_url}/search?q={query}") as response:
                self._validate_failed_request(response.status)                
                data = await response.json()
                return self._map_places(data)