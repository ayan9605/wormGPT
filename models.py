from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str

class ConfigUpdate(BaseModel):
    api_key: Optional[str] = None
    model: Optional[str] = None
    language: Optional[str] = None
