from pydantic import BaseModel


class User(BaseModel):
    user_id: str


class Pair(BaseModel):
    id: str
    left: str
    right: str
