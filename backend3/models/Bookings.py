from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Bookings(BaseModel):
    BookingID: int
    StudentID: int
    RoomChoice: str
    TimeIn: datetime
    TimeOut: datetime
    Companions: Optional[str]
