from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
from datetime import datetime
from datetime import datetime, timedelta
import json
from typing import List


bookings = APIRouter(tags=["For Bookings"])

@bookings.get('/bookings/all_bookings', response_model=List[dict])
async def get_all_bookings(db_tuple: tuple = Depends(get_db)):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    query = """
        SELECT bookings.*, students.Name AS StudentName
        FROM bookings
        JOIN students ON bookings.StudentID = students.StudentID
    """
    cursor.execute(query)
    bookings = cursor.fetchall()

    response = []
    for booking in bookings:
        companions = booking[5]  # Get the companions JSON string
        if companions:
            try:
                companions_list = json.loads(companions)
            except json.JSONDecodeError:
                companions_list = []  # Set empty list if companions JSON string is invalid
        else:
            companions_list = []  # Set empty list if companions JSON string is empty
        response.append({
            "BookingID": booking[0],
            "StudentID": booking[1],
            "RoomChoice": booking[2],
            "TimeIn": booking[3],
            "TimeOut": booking[4],
            "Companions": companions_list,  # Use deserialized companions list
            "StudentName": booking[6]  # Student name from the join
        })

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    return response

@bookings.get('/bookings/weekly_bookings', response_model=List[dict])
async def get_weekly_bookings(db_tuple: tuple = Depends(get_db)):
    cursor, db = db_tuple

    # Get the current date
    current_date = datetime.now().date()

    # Calculate the start and end dates of the week
    start_of_week = current_date - timedelta(days=current_date.weekday())  # Assuming the week starts on Sunday
    end_of_week = start_of_week + timedelta(days=6)

    # Format the dates as strings
    start_of_week_str = start_of_week.strftime("%Y-%m-%d")
    end_of_week_str = end_of_week.strftime("%Y-%m-%d")

    # Fetch bookings within the week
    query = """
        SELECT bookings.*, students.Name AS StudentName
        FROM bookings
        JOIN students ON bookings.StudentID = students.StudentID
        WHERE DATE(bookings.TimeIn) BETWEEN %s AND %s
    """
    cursor.execute(query, (start_of_week_str, end_of_week_str))
    bookings = cursor.fetchall()

    response = []
    for booking in bookings:
        companions = booking[5]  # Get the companions JSON string
        if companions:
            try:
                companions_list = json.loads(companions)
            except json.JSONDecodeError:
                companions_list = []  # Set empty list if companions JSON string is invalid
        else:
            companions_list = []  # Set empty list if companions JSON string is empty
        response.append({
            "BookingID": booking[0],
            "StudentID": booking[1],
            "RoomChoice": booking[2],
            "TimeIn": booking[3],
            "TimeOut": booking[4],
            "Companions": companions_list,  # Use deserialized companions list
            "StudentName": booking[6]  # Student name from the join
        })

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    return response

@bookings.get('/bookings/find_booking', response_model=dict)
async def find_booking(booking_id: int, db_tuple: tuple = Depends(get_db)):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    query = """
        SELECT bookings.*, students.Name AS StudentName
        FROM bookings
        JOIN students ON bookings.StudentID = students.StudentID
        WHERE bookings.BookingID = %s
    """
    cursor.execute(query, (booking_id,))
    booking = cursor.fetchone()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    response = {
        "BookingID": booking[0],
        "StudentID": booking[1],
        "RoomChoice": booking[2],
        "TimeIn": booking[3],
        "TimeOut": booking[4],
        "Companions": json.loads(booking[5]),  # Deserialize JSON string to list
        "StudentName": booking[6]  # Student name from the join
    }

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    return response

from datetime import datetime, timedelta
from fastapi import HTTPException

@bookings.post('/bookings/create_booking', status_code=201, response_model=dict)
async def create_booking_schedule(
    username: str,
    room_choice: int,
    time_in: str,
    time_out: str,
    companions: str,
    db_tuple: tuple = Depends(get_db)
):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    # Retrieve StudentID based on username
    query_get_studentID = "SELECT StudentID FROM students WHERE Username = %s"
    cursor.execute(query_get_studentID, (username,))
    student = cursor.fetchone()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    studentID = student[0]  # Extract the StudentID from the result

    # Parse time_in and time_out to datetime objects
    try:
        time_in_parsed = datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S")
        time_out_parsed = datetime.strptime(time_out, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format. Please use format 'YYYY-MM-DD HH:MM:SS'.")

    # Check if the booking duration exceeds 2 hours
    if time_out_parsed - time_in_parsed > timedelta(hours=2):
        raise HTTPException(status_code=400, detail="Booking duration cannot exceed 2 hours.")

    # Check for double booking for the specified room
    query_check_double_booking = """
        SELECT COUNT(*) FROM bookings 
        WHERE RoomChoice = %s 
        AND ((TimeIn BETWEEN %s AND %s) OR (TimeOut BETWEEN %s AND %s))
    """
    cursor.execute(query_check_double_booking, (room_choice, time_in_parsed, time_out_parsed, time_in_parsed, time_out_parsed))
    booking_count = cursor.fetchone()[0]

    if booking_count > 0:
        raise HTTPException(status_code=400, detail="Double booking detected for the specified room.")

    # Convert companions list to JSON
    companions_json = json.dumps(companions)

    # Insert the booking schedule into the database
    query_insert_booking = """
        INSERT INTO bookings 
        (StudentID, RoomChoice, TimeIn, TimeOut, Companions) 
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query_insert_booking, (
        studentID,  # Use the retrieved StudentID
        room_choice,
        time_in_parsed.strftime("%Y-%m-%d %H:%M:%S"),  # Format datetime object as string
        time_out_parsed.strftime("%Y-%m-%d %H:%M:%S"),  # Format datetime object as string
        companions_json  # Insert JSON string instead of list
    ))
    db.commit()

    # Get the auto-incremented BookingID
    bookingID = cursor.lastrowid

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    # Construct and return the response
    new_booking = {
        "BookingID": bookingID,
        "StudentID": studentID,
        "RoomChoice": room_choice,
        "TimeIn": time_in_parsed.strftime("%Y-%m-%d %H:%M:%S"),  # Format datetime object as string
        "TimeOut": time_out_parsed.strftime("%Y-%m-%d %H:%M:%S"),  # Format datetime object as string
        "Companions": companions
    }

    return new_booking




@bookings.put('/bookings/edit/{booking_id}', response_model=dict)
async def edit_booking(
    booking_id: int,
    student_id: int,
    password: str = Form(...),  # Required password field
    new_room_choice: int = Form(None),  # Optional new room choice field
    new_time_in: str = Form(None),  # Optional new time in field
    new_time_out: str = Form(None),  # Optional new time out field
    new_companions: str = Form(None),  # Optional new companions field
    db_tuple: tuple = Depends(get_db)
):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    # Check if the booking exists and the password is correct
    query_check_booking = """
        SELECT * FROM bookings 
        JOIN students ON bookings.StudentID = students.StudentID 
        WHERE BookingID = %s AND bookings.StudentID = %s AND students.Password = %s
    """
    cursor.execute(query_check_booking, (booking_id, student_id, password))
    existing_booking = cursor.fetchone()
    if not existing_booking:
        raise HTTPException(status_code=404, detail="Incorrect booking ID, student ID, or password")

    # Construct the query based on the provided fields
    update_values = {}
    if new_room_choice is not None:
        update_values["RoomChoice"] = new_room_choice
    if new_time_in:
        update_values["TimeIn"] = new_time_in
    if new_time_out:
        update_values["TimeOut"] = new_time_out
    if new_companions:
        update_values["Companions"] = new_companions

    # Check if any fields are provided for update
    if not update_values:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    # Construct the UPDATE query
    query_update_booking = "UPDATE bookings SET "
    query_update_booking += ", ".join([f"{field} = %s" for field in update_values])
    query_update_booking += " WHERE BookingID = %s"

    # Execute the UPDATE query
    cursor.execute(query_update_booking, list(update_values.values()) + [booking_id])
    db.commit()  # Commit changes

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    # Return the updated booking information
    updated_booking = {
        "BookingID": booking_id,
        **update_values
    }
    return updated_booking

@bookings.delete('/bookings/delete/{booking_id}', status_code=204)
async def delete_booking(booking_id: int, db_tuple: tuple = Depends(get_db)):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    # Check if the booking exists
    query_check_booking = "SELECT * FROM bookings WHERE BookingID = %s"
    cursor.execute(query_check_booking, (booking_id,))
    existing_booking = cursor.fetchone()
    if not existing_booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Delete the booking
    query_delete_booking = "DELETE FROM bookings WHERE BookingID = %s"
    cursor.execute(query_delete_booking, (booking_id,))
    db.commit()  # Commit changes

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    # Return 204 No Content on successful deletion
    return



