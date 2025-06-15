from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from enums.RoleEnum import Role

class User(BaseModel):
    _id: str
    name: str
    email: str
    password: str
    gender: str
    ethnicity: str
    age: int
    enrollment: str
    roles: list[Role] = None
