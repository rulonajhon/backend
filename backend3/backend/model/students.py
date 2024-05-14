#students.py

from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db


students = APIRouter(tags=["For Students"])


@students.get('/student/list', response_model=list)
async def student_list(db_tuple: tuple = Depends(get_db)):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    query = "SELECT StudentID, Username, Password, Name, Email from students"
    cursor.execute(query)
    users = [
        {"StudentID": user[0], "Username": user[1], "Password": user[2], "Name": user[3], "Email": user[4]}
        for user in cursor.fetchall()
    ]

    db.commit()  # Commit changes if any
    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    return users

@students.get('/student/find_student', response_model=dict)
async def find_student(student_id: int, db_tuple: tuple = Depends(get_db)):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    query = "SELECT StudentID, Username, Password, Name, Email FROM students WHERE StudentID = %s"
    cursor.execute(query, (student_id,))
    user = cursor.fetchone()

    if user:
        student = {
            "StudentID": user[0],
            "Username": user[1],
            "Password": user[2],
            "Name": user[3],
            "Email": user[4]
        }
        return student
    else:
        return {"message": "Student not found"}

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection



@students.post('/student/create', status_code=201, response_model=dict)
async def create_student(
    studentID: int,
    username: str,
    password: str,
    name: str,
    email: str,
    db_tuple: tuple = Depends(get_db)
):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    # Check if the username already exists
    query_check_username = "SELECT * FROM students WHERE Username = %s"
    cursor.execute(query_check_username, (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Insert the new student into the database with the provided Student_ID
    query_insert_student = "INSERT INTO students (StudentID, Username, Password, Name, Email) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query_insert_student, (studentID, username, password, name, email))
    db.commit()

    # Construct and return the response
    new_student = {
        "StudentID": studentID,
        "Username": username,
        "Password": password,
        "Name": name,
        "Email": email
    }

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    return new_student

from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

@students.post('/student/login', response_model=dict)
async def student_login(
    login_request: LoginRequest,
    db_tuple: tuple = Depends(get_db)
):
    username = login_request.username
    password = login_request.password
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    # Check if the username and password match
    query_login = "SELECT StudentID, Username, Name, Email FROM students WHERE Username = %s AND Password = %s"
    cursor.execute(query_login, (username, password))
    user = cursor.fetchone()

    if user:
        student = {
            "StudentID": user[0],
            "Username": user[1],
            "Name": user[2],
            "Email": user[3]
        }
        return {"message": "Login successful", "student": student}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    cursor.close()  # Close the cursor
    db.close()  

@students.put('/student/edit/{student_id}', response_model=dict)
async def edit_student(
    student_id: int,
    password: str = Form(...),  # Required password field
    new_username: str = Form(None),  # Optional new username field
    new_password: str = Form(None),  # Optional new password field
    new_name: str = Form(None),  # Optional new name field
    new_email: str = Form(None),  # Optional new email field
    db_tuple: tuple = Depends(get_db)
):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    # Check if the student exists and the password is correct
    query_check_student = "SELECT * FROM students WHERE StudentID = %s AND Password = %s"
    cursor.execute(query_check_student, (student_id, password))
    existing_student = cursor.fetchone()
    if not existing_student:
        raise HTTPException(status_code=404, detail="Incorrect student ID or password")

    # Construct the query based on the provided fields
    update_values = {}
    if new_username:
        update_values["Username"] = new_username
    if new_password:
        update_values["Password"] = new_password
    if new_name:
        update_values["Name"] = new_name
    if new_email:
        update_values["Email"] = new_email

    # Check if any fields are provided for update
    if not update_values:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    # Construct the UPDATE query
    query_update_student = "UPDATE students SET "
    query_update_student += ", ".join([f"{field} = %s" for field in update_values])
    query_update_student += " WHERE StudentID = %s"

    # Execute the UPDATE query
    cursor.execute(query_update_student, list(update_values.values()) + [student_id])
    db.commit()  # Commit changes

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    # Return the updated student information
    updated_student = {
        "StudentID": student_id,
        **update_values
    }
    return updated_student

@students.delete('/student/delete/{student_id}', status_code=204)
async def delete_student(student_id: int, db_tuple: tuple = Depends(get_db)):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    # Check if the student exists
    query_check_student = "SELECT * FROM students WHERE StudentID = %s"
    cursor.execute(query_check_student, (student_id,))
    existing_student = cursor.fetchone()
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Delete the student
    query_delete_student = "DELETE FROM students WHERE StudentID = %s"
    cursor.execute(query_delete_student, (student_id,))
    db.commit()  # Commit changes

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    # Return 204 No Content on successful deletion
    return