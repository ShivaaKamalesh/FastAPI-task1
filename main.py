from fastapi import FastAPI
from pydantic import BaseModel,EmailStr
from fastapi import HTTPException, status

import mysql.connector

app=FastAPI()

conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="home@1234",
    database="revature2"
)

cursor=conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS user5(
        id INT PRIMARY KEY,
        username VARCHAR(50),
        email VARCHAR(50),
        password VARCHAR(50)   
    );
""")
conn.commit()

cursor.execute("""
INSERT IGNORE INTO user5 (id, username, email, password) VALUES
(1, 'alice_green', 'alice.green@example.com', 'alice@123'),
(2, 'robert_white', 'robert.white@example.com', 'robert@456'),
(3, 'olivia_clark', 'olivia.clark@example.com', 'olivia@789'),
(4, 'daniel_moore', 'daniel.moore@example.com', 'daniel@321'),
(5, 'grace_hall', 'grace.hall@example.com', 'grace@654');
""")
conn.commit()

class User(BaseModel):
    id:int
    username:str
    email:EmailStr
    password:str

# adding user to db
@app.post("/user")
def add_user(user:User):
    cursor.execute(
        "INSERT INTO user5 (id, username, email, password) VALUES (%s, %s, %s, %s)",
        (user.id, user.username, user.email, user.password)
    )
    conn.commit()
    return {"message": "User added successfully!"}

# update using query
@app.put("/user/{id}")
def upd_details(id:int,user:User):
    cursor.execute("Select * from user5 where id=%s",(id,))
    exist=cursor.fetchone()
    if not exist:
        raise HTTPException(status_code=404, detail="User not found")
    
    cursor.execute(
        "UPDATE user5 SET username=%s, email=%s, password=%s WHERE id=%s",
        (user.username, user.email, user.password, id)
    )
    conn.commit()
    return {"message": "User updated successfully!"}

# Read all users

@app.get("/users")
def get_alluser():
    cursor.execute("select * from user5")
    existt=cursor.fetchall()
    return{"details":existt}


# validation
@app.get("/userss")
def get_alluser(limit: int = 10):
    cursor.execute("SELECT * FROM user5 LIMIT %s", (limit,))
    users = cursor.fetchall()
    return {"details": users}

# delete

@app.delete("/usersss/{id}")
def delete(id:int):
    cursor.execute("Select * from user5 where id=%s",(id,))
    dexist=cursor.fetchone()
    if not dexist:
        raise HTTPException(status_code=404, detail="User not found")
    
    cursor.execute("Delete from user5 where id=%s",(id,))

    conn.commit()
    return {"message": "User deleted successfully!"}

    
