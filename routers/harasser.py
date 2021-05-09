from typing import Any, List, Union
import peewee
import datetime
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.harasser import create_harasser, get_harasser, get_harasser_by_username, list_harassers, delete_harasser, add_record
from pydantic import BaseModel
from pydantic.utils import GetterDict
from fastapi import APIRouter

router_harassers = APIRouter(
    prefix="/harasser",
    tags=["harassers"]
)


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class HarasserModel(BaseModel):
    id: int
    username: str
    platform: str
    record: int
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


@router_harassers.get("/", response_model=List[HarasserModel], summary="List of harassers",
                      description="Returns all harassers")
def get_harassers():
    return list_harassers()


@router_harassers.get("/{username}", response_model=HarasserModel, summary="Returns a single harasser")
async def view(username: str):
    """
        To view all details related to a single harasser
        - **username**: The username of the harasser you want to view details.
    """
    harasser = get_harasser_by_username(username=username)
    if harasser is None:
        raise HTTPException(status_code=404, detail="harasser not found")

    return harasser


@router_harassers.post("/", response_model=HarasserModel, summary="Create a new harasser")
async def create(username: str, platform: str):
    harasser = get_harasser_by_username(username=username)
    if harasser is None:
        return await create_harasser(username=username, platform=platform)
    return add_record(id=harasser.id)


@router_harassers.delete(
    "/remove/{id}",
    summary="Delete an individual harasser",
    response_class=Response,
    responses={
        200: {"description": "harasser successfully deleted"},
        404: {"description": "harasser not found"},
    },
)
def remove_harasser(id: int):
    del_harasser = delete_harasser(id)
    if del_harasser is None:
        return Response(status_code=404)
    return Response(status_code=200)
