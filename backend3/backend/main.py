# main.py


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model.users import router
from model.students import students
from model.admins import admins
from model.bookings import bookings
from model.bookinghistory import bookinghistory

app = FastAPI()

# Define allowed origins
origins = [
    "http://localhost",
    "http://localhost:5174"
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/users")
app.include_router(students, prefix="/users")
app.include_router(admins, prefix="/admin")
app.include_router(bookings, prefix="/bookings")
app.include_router(bookinghistory, prefix="/bookinghistory")
