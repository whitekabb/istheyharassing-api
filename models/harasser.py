from peewee import *
from .Base import BaseModel
import datetime

class Harasser(BaseModel):
    id = PrimaryKeyField(null=False)
    username = CharField(max_length=30)
    platform = CharField(max_length=30)
    record = BigIntegerField()
    updated_at = DateTimeField()

class Meta:
        db_table = 'harassers'

async def create_harasser(username: str, platform: str):
    harasser_object = Harasser(
        username=username,
        platform=platform,
        record=1,
        updated_at=datetime.datetime.now()
    )
    harasser_object.save()
    return harasser_object


def get_harasser(id: int):
    return Harasser.filter(Harasser.id == id).first()

def get_harasser_by_username(username: str):
    return Harasser.filter(Harasser.username == username).first()

def list_harassers(skip: int = 0, limit: int = 100):
    return list(Harasser.select().offset(skip).limit(limit))

def add_record(id: int):
    harasser_object = get_harasser(id=id)
    harasser_object.record += 1
    harasser_object.updated_at=datetime.datetime.now()
    harasser_object.save()
    return harasser_object

def delete_harasser(id: int):
    return Harasser.delete().where(Harasser.id == id).execute()

