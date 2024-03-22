from pydantic import BaseModel
from datetime import datetime
class BookingHistory(BaseModel):
    HistoryID: int
    BookingID: int
    StudentID: int
    RoomChoice: str
    TimeIn: datetime
    TimeOut: datetime
    Companions: str