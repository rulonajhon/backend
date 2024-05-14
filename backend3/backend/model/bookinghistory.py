from fastapi import Depends, HTTPException, APIRouter
from .db import get_db
import json
from typing import List

bookinghistory = APIRouter(tags=["Booking History"])

@bookinghistory.get('/bookings/all_booking_history', response_model=List[dict])
async def get_all_booking_history(db_tuple: tuple = Depends(get_db)):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    query = """
        SELECT bookinghistory.*, students.Name AS StudentName
        FROM bookinghistory
        JOIN students ON bookinghistory.StudentID = students.StudentID
    """
    cursor.execute(query)
    booking_history = cursor.fetchall()

    response = []
    for history in booking_history:
        companions = history[5]  # Get the companions JSON string
        if isinstance(companions, str):
            companions_list = json.loads(companions)
        else:
            companions_list = []  # Set empty list if companions is not a string
        response.append({
            "BookingID": history[0],
            "StudentID": history[1],
            "RoomChoice": history[2],
            "TimeIn": history[3],
            "TimeOut": history[4],
            "Companions": companions_list,
            "StudentName": history[6]
        })

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    return response



@bookinghistory.post("/bookings/booking_history", status_code=201)
async def create_booking_history(booking_id: int, db_tuple: tuple = Depends(get_db)):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    # Check if the bookingID already exists in the booking history table
    query_check_duplicate = """
        SELECT *
        FROM bookinghistory
        WHERE BookingID = %s
    """
    cursor.execute(query_check_duplicate, (booking_id,))
    existing_booking = cursor.fetchone()

    if existing_booking:
        raise HTTPException(status_code=400, detail="Booking history already exists for this bookingID")

    # Retrieve booking information based on the provided booking_id
    query_select_booking = """
        SELECT *
        FROM bookings
        WHERE BookingID = %s
    """
    cursor.execute(query_select_booking, (booking_id,))
    booking = cursor.fetchone()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Insert the booking information into the booking history table
    query_insert_history = """
        INSERT INTO bookinghistory (BookingID, StudentID, RoomChoice, TimeIn, TimeOut, Companions)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query_insert_history, (
        booking[0],  # BookingID
        booking[1],  # StudentID
        booking[2],  # RoomChoice
        booking[3],  # TimeIn
        booking[4],  # TimeOut
        booking[5]   # Companions
    ))
    db.commit()

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    return {"message": "Booking history created successfully"}

@bookinghistory.delete("/bookinghistory/delete/{booking_id}")
async def delete_booking_history(booking_id: int, db_tuple: tuple = Depends(get_db)):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    # Check if the booking history exists
    query_check_booking = "SELECT * FROM bookinghistory WHERE BookingID = %s"
    cursor.execute(query_check_booking, (booking_id,))
    existing_booking = cursor.fetchone()
    if not existing_booking:
        raise HTTPException(status_code=404, detail="Booking history not found")

    # Delete the booking history
    query_delete_booking = "DELETE FROM bookinghistory WHERE BookingID = %s"
    cursor.execute(query_delete_booking, (booking_id,))
    db.commit()  # Commit changes

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    return {"message": "Booking history deleted successfully"}