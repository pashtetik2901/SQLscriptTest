from pydantic import BaseModel

class MainResponse(BaseModel):
    status: bool = True or False