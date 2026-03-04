# fastapi_app/models/__init__.py
from pydantic import BaseModel
class Note(BaseModel):
    title: str
    content: str
