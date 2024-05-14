# main.py

from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from models.Students import Students
from models.Admins import Admins
from models.Bookings import Bookings

import mysql.connector

# Database configuration - A function to create a connection to the database
def create_connection():
    db_config = {
         "host": "localhost",
         "user": "root",
         "password": "",
         "database": "crbs3",
         "port": 3306
     } 
    return mysql.connector.connect(**db_config)

# FastAPI app
app = FastAPI()

# API endpoint to get all student
@app.get("/students/", response_model=list[Students], tags=["Student"])
async def get_student():
    try:
        # Create a connection to the database
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)

        # Execute SQL query to fetch all student
        cursor.execute("SELECT * FROM Students")
        UserAccount = cursor.fetchall()
        return UserAccount
    except mysql.connector.Error as e:
        # Handle MySQL errors
        return JSONResponse(content={"error": f"MySQL Error: {e}"}, status_code=500)
    except Exception as e:
        # Handle other exceptions
        return JSONResponse(content={"error": f"Error: {e}"}, status_code=500)
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

# PUT endpoint to add a new student
@app.post("/students/", response_model=Students, tags=["Student"])
async def create_student(student: Students = Body(...)):
    try:
        # Create a connection to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Execute SQL query to insert new student
        cursor.execute("""
            INSERT INTO Students (studentID, Username, Password, Name, Email)
            VALUES (%s,%s, %s, %s, %s)
        """, (student.StudentID,student.Username, student.Password, student.Name, student.Email))
        conn.commit()

        return student
    except mysql.connector.Error as e:
        # Handle MySQL errors
        return JSONResponse(content={"error": f"MySQL Error: {e}"}, status_code=500)
    except Exception as e:
        # Handle other exceptions
        return JSONResponse(content={"error": f"Error: {e}"}, status_code=500)
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

@app.put("/students/{student_id}", tags=["Student"])
async def edit_student(student_id: int, student: Students = Body(...)):
    try:
        # Create a connection to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Execute SQL query to update student information
        cursor.execute("""
            UPDATE Students
            SET Username = %s, Password = %s, Name = %s, Email = %s
            WHERE StudentID = %s
        """, (student.Username, student.Password, student.Name, student.Email, student_id))
        conn.commit()

        # Check if any rows were affected (i.e., if student existed and was updated)
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"message": "Student information updated successfully", "updated_student": student}
    except mysql.connector.Error as e:
        # Handle MySQL errors
        return HTTPException(status_code=500, detail=f"MySQL Error: {e}")
    except Exception as e:
        # Handle other exceptions
        return HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

@app.delete("/students/{student_id}", tags=["Student"])
async def delete_student(student_id: int):
    try:
        # Create a connection to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Execute SQL query to delete student information
        cursor.execute("DELETE FROM Students WHERE StudentID = %s", (student_id,))
        conn.commit()

        # Check if any rows were affected (i.e., if student existed and was deleted)
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"message": "Student information deleted successfully"}
    except mysql.connector.Error as e:
        # Handle MySQL errors
        return HTTPException(status_code=500, detail=f"MySQL Error: {e}")
    except Exception as e:
        # Handle other exceptions
        return HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

@app.get("/admins/", response_model=list[Admins], tags=["Admin"])
async def get_admin():
    try:
        # Create a connection to the database
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)

        # Execute SQL query to fetch all student
        cursor.execute("SELECT * FROM Admins")
        Admin = cursor.fetchall()
        return Admin
    except mysql.connector.Error as e:
        # Handle MySQL errors
        return JSONResponse(content={"error": f"MySQL Error: {e}"}, status_code=500)
    except Exception as e:
        # Handle other exceptions
        return JSONResponse(content={"error": f"Error: {e}"}, status_code=500)
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

@app.get("/bookings/", response_model=list[Bookings], tags=["Booking"])
async def get_booking():
    try:
        # Create a connection to the database
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)

        # Execute SQL query to fetch all student
        cursor.execute("SELECT * FROM Bookings")
        Booking = cursor.fetchall()
        return Booking
    except mysql.connector.Error as e:
        # Handle MySQL errors
        return JSONResponse(content={"error": f"MySQL Error: {e}"}, status_code=500)
    except Exception as e:
        # Handle other exceptions
        return JSONResponse(content={"error": f"Error: {e}"}, status_code=500)
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

# PUT endpoint to add a new admin
@app.put("/admins/", response_model=Admins, tags=["Admin"])
async def create_admin(admin: Admins = Body(...)):
    try:
        # Create a connection to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Execute SQL query to insert new admin
        cursor.execute("""
            INSERT INTO Admins (Username, Password)
            VALUES (%s, %s)
        """, (admin.Username, admin.Password))
        conn.commit()

        return admin
    except mysql.connector.Error as e:
        # Handle MySQL errors
        return JSONResponse(content={"error": f"MySQL Error: {e}"}, status_code=500)
    except Exception as e:
        # Handle other exceptions
        return JSONResponse(content={"error": f"Error: {e}"}, status_code=500)
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

# PUT endpoint to add a new booking
@app.post("/bookings/", response_model=Bookings, tags=["Booking"])
async def create_booking(booking: Bookings = Body(...)):
    try:
        # Create a connection to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Execute SQL query to insert new booking
        cursor.execute("""
            INSERT INTO Bookings (StudentID, RoomChoice, TimeIn, TimeOut, Companions)
            VALUES (%s, %s, %s, %s, %s)
        """, (booking.StudentID, booking.RoomChoice, booking.TimeIn, booking.TimeOut, booking.Companions))
        conn.commit()

        return booking
    except mysql.connector.Error as e:
        # Handle MySQL errors
        return JSONResponse(content={"error": f"MySQL Error: {e}"}, status_code=500)
    except Exception as e:
        # Handle other exceptions
        return JSONResponse(content={"error": f"Error: {e}"}, status_code=500)
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

# PUT method to copy booking to booking history using BookingID
@app.put("/bookings/{bookingID}/copy", tags=["History"])
async def copy_booking_to_history(bookingID: int):
    try:
        # Create a connection to the database
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)

        # Retrieve booking details based on BookingID
        cursor.execute("SELECT * FROM Bookings WHERE BookingID = %s", (bookingID,))
        booking = cursor.fetchone()

        if booking:
            # Insert booking details into BookingHistory table
            cursor.execute("""
                INSERT INTO BookingHistory (BookingID, StudentID, RoomChoice, TimeIn, TimeOut, Companions)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (booking['BookingID'], booking['StudentID'], booking['RoomChoice'], booking['TimeIn'], booking['TimeOut'], booking['Companions']))
            conn.commit()

            return {"message": f"Booking with BookingID {bookingID} copied to BookingHistory"}
        else:
            raise HTTPException(status_code=404, detail=f"Booking with BookingID {bookingID} not found")
    except mysql.connector.Error as e:
        # Handle MySQL errors
        raise HTTPException(status_code=500, detail=f"MySQL Error: {e}")
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

from fastapi import HTTPException

@app.delete("/admins/{admin_id}", tags=["Admin"])
async def delete_admin(admin_id: int):
    try:
        # Create a connection to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Execute SQL query to delete admin information
        cursor.execute("DELETE FROM Admins WHERE AdminID = %s", (admin_id,))
        conn.commit()

        # Check if any rows were affected (i.e., if admin existed and was deleted)
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Admin not found")

        return {"message": "Admin account deleted successfully"}
    except mysql.connector.Error as e:
        # Handle MySQL errors
        raise HTTPException(status_code=500, detail=f"MySQL Error: {e}")
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

@app.get("/history/bookings/", tags=["History"])
async def get_booking_history():
    try:
        # Create a connection to the database
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)

        # Execute SQL query to fetch booking history
        cursor.execute("SELECT * FROM BookingHistory")
        history = cursor.fetchall()
        return history
    except mysql.connector.Error as e:
        # Handle MySQL errors
        raise HTTPException(status_code=500, detail=f"MySQL Error: {e}")
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

@app.put("/admins/{admin_id}", tags=["Admin"])
async def edit_admin(admin_id: int, admin: Admins = Body(...)):
    try:
        # Create a connection to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Execute SQL query to update admin information
        cursor.execute("""
            UPDATE Admins
            SET Username = %s, Password = %s
            WHERE AdminID = %s
        """, (admin.Username, admin.Password, admin_id))
        conn.commit()

        # Check if any rows were affected (i.e., if admin existed and was updated)
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Admin not found")

        return {"message": "Admin information updated successfully", "updated_admin": admin}
    except mysql.connector.Error as e:
        # Handle MySQL errors
        raise HTTPException(status_code=500, detail=f"MySQL Error: {e}")
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

@app.put("/bookings/{booking_id}", tags=["Booking"])
async def edit_booking(booking_id: int, booking: Bookings = Body(...)):
    try:
        # Create a connection to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Execute SQL query to update booking information
        cursor.execute("""
            UPDATE Bookings
            SET RoomChoice = %s, TimeIn = %s, TimeOut = %s, Companions = %s
            WHERE BookingID = %s
        """, (booking.RoomChoice, booking.TimeIn, booking.TimeOut, booking.Companions, booking_id))
        conn.commit()

        # Check if any rows were affected (i.e., if booking existed and was updated)
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Booking not found")

        return {"message": "Booking information updated successfully", "updated_booking": booking}
    except mysql.connector.Error as e:
        # Handle MySQL errors
        raise HTTPException(status_code=500, detail=f"MySQL Error: {e}")
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        # Close the cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

