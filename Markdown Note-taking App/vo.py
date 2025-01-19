from pydantic import BaseModel

class NoteRequest(BaseModel):
    content: str