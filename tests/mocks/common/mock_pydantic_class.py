from typing import List

from pydantic import BaseModel, PositiveInt


class Request(BaseModel):
    test_id: str 
    fail_id: str 
    object_key: dict[str, str]
    array_number: List[PositiveInt]  
    array_objects: List[dict[str, PositiveInt]]


class UserRequest(BaseModel):
    id: PositiveInt 
    email: str
    active: bool 
    favorites: List[str]
    notification_config: dict[str, bool]