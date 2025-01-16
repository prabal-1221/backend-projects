from pydantic import BaseModel

class TaskRequest(BaseModel):
    title: str
    description: str