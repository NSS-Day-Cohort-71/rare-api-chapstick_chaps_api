import sqlite3
import json


def get_categories():

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT 
                c.id, 
                c.label
            FROM Categories c
        """
        )

        query_results = db_cursor.fetchall()
        categories = []
        for row in query_results:
            categories.append(dict(row))

        serialized_categories = json.dumps(categories)
    return serialized_categories

def create_category(category):
    with sqlite3.connect("./db.sqlite3") as conn: # Connect to the database
        conn.row_factory = sqlite3.Row # Set the row factory to use sqlite3.Row
        db_cursor = conn.cursor()

        # Execute the SQL query to insert the new category
        db_cursor.execute(
            """
            INSERT INTO Categories (label)
            VALUES (?)
            """,
            (category["label"],),
        )

        # Get the id of the row that was just inserted
        id = db_cursor.lastrowid

        # Return the id in a json string
        return json.dumps({"category_id": id})