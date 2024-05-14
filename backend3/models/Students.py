from pydantic import BaseModel

class Students(BaseModel):
    StudentID: int
    Username: str
    Password: str
    Name: str
    Email: str
