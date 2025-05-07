from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

DATABASE_URL = "acc_auth.db"  # Replace with your actual database file

# Define a Pydantic model for your data (adjust fields accordingly)
class UserACCGroup(BaseModel):
    username: str
    accgroup: str


def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_URL)
    except sqlite3.Error as e:
        print(e)
    return conn


@app.get("/items/{username}", response_model=UserACCGroup)
async def read_item(username: str):
    """
    Retrieves an item from the database by its ID.
    """
    print(username)
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    cursor = conn.cursor()
    cursor.execute("SELECT username, accgroup FROM UserACCGroup WHERE username=?", (username,))  # Adjust query
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Convert the row to a dictionary and then to a Pydantic model
    item_data = {
        "username": row[0],
        "accgroup": row[1]
    }
    return UserACCGroup(**item_data)


@app.get("/items/", response_model=list[UserACCGroup])
async def read_all_items():
    """
    Retrieves all items from the database.
    """
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    cursor = conn.cursor()
    cursor.execute("SELECT username, accgroup FROM UserACCGroup") #Adjust query
    rows = cursor.fetchall()
    conn.close()

    items = []
    for row in rows:
         item_data = {
            "username": row[0],
            "accgroup": row[1]
        }
         items.append(UserACCGroup(**item_data)) # type: ignore

    return items


# Example POST endpoint (for creating new items)
@app.post("/items/", response_model=UserACCGroup, status_code=201)
async def create_item(item: UserACCGroup):
    """
    Creates a new item in the database.
    """
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO UserACCGroup (username, accgroup) VALUES (?, ?)",  # Adjust query
            (item.username, item.accgroup),
        )
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {e}")
    finally:
        conn.close()

    return item



# Example of how to create the table (if it doesn't exist) -  RUN THIS ONCE
def create_table():
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database")
        return

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserACCGroup (
            username TEXT NOT NULL,
            accgroup TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    print('Running Scripts')
    # Run this once to create the table
    create_table()  #VERY IMPORTANT: Create the table *before* running the FastAPI app
    #  To run the app:  `uvicorn main:app --reload`  (assuming this code is in main.py)

    #The below is just example dummy data for testing.  Remove or comment out for production.
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM UserACCGroup") #Clear out old data.
    cursor.execute("INSERT INTO UserACCGroup (username, accgroup) VALUES ('spalagir', 'Easy Flow')")
    cursor.execute("INSERT INTO UserACCGroup (username, accgroup) VALUES ('bfreedman', 'Easy Flow')")
    cursor.execute("INSERT INTO UserACCGroup (username, accgroup) VALUES ('jpain', 'Easy Flow')")
    conn.commit()
    conn.close()
