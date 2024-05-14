from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db


admins = APIRouter(tags=["For Admin"])


@admins.get('/admin/list', response_model=list)
async def admin_list(
    db_tuple: tuple = Depends(get_db)
    ):
    
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    query = "SELECT AdminID, Username, Password from admins"
    cursor.execute(query)
    users = [
        {"AdminID": user[0], "Username": user[1], "Password": user[2]}
        for user in cursor.fetchall()
        
    ]
    db.commit()  # Commit changes if any
    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    return users


@admins.get('/admin/find_admin', response_model=dict)
async def find_admin(
    AdminID: int, 
    db_tuple: tuple = Depends(get_db)
    ):
   
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    query = "SELECT AdminID, Username, Password FROM admins WHERE AdminID = %s"
    cursor.execute(query, (AdminID,))
    user = cursor.fetchone()

    if user:
        student = {
            "AdminID": user[0],
            "Username": user[1],
            "Password": user[2],
        }
        return student
    else:
        return {"message": "Admin not found"}

    cursor.close()  # Close the cursor
    db.close()  # Close the database


@admins.post('/admin/create', status_code=201, response_model=dict)
async def create_admin(
    username: str,
    password: str,
    db_tuple: tuple = Depends(get_db)
):
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    # Check if the username already exists
    query_check_username = "SELECT * FROM admins WHERE Username = %s"
    cursor.execute(query_check_username, (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Insert the new student into the database
    query_insert_admin = "INSERT INTO admins (Username, Password) VALUES (%s, %s)"
    cursor.execute(query_insert_admin, (username, password))
    db.commit()

    # Construct and return the response
    new_admin_id = cursor.lastrowid  # Retrieve the auto-generated AdminID
    new_admin = {
        "AdminID": new_admin_id,
        "Username": username,
        "Password": password,
    }

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    return new_admin


from pydantic import BaseModel



class LoginRequest(BaseModel):
    username: str
    password: str

@admins.post('/admin/login', response_model=dict)
async def admin_login(
    login_request: LoginRequest,
    db_tuple: tuple = Depends(get_db)
):
    username = login_request.username
    password = login_request.password
    cursor, db = db_tuple  # Unpack the tuple returned by get_db into cursor and db

    # Check if the provided username exists in the database
    query_check_username = "SELECT * FROM admins WHERE Username = %s"
    cursor.execute(query_check_username, (username,))
    admin = cursor.fetchone()

    if admin:
        # Verify the password
        if admin[2] == password:  # Assuming the password is stored in the third column of the result
            # Here, you can generate a token or session to represent the authenticated admin
            # For simplicity, let's return the admin details
            admin_data = {
                "AdminID": admin[0],
                "Username": admin[1],
                # Exclude password for security reasons
            }
            return {"message": "Login successful", "admin": admin_data}

    # If the username or password is incorrect, raise an HTTPException
    raise HTTPException(status_code=401, detail="Invalid username or password")

    cursor.close()
    db.close()

