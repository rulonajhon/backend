from pydantic import BaseModel
class Admins(BaseModel):
    AdminID: int
    Username: str
    Password:str 