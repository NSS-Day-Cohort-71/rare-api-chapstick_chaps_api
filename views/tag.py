import sqlite3
import json


def get_tags():

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT 
                t.id, 
                t.label
            FROM Tags t
        """
        )

        query_results = db_cursor.fetchall()
        tags = []
        for row in query_results:
            tags.append(dict(row))

        serialized_tags = json.dumps(tags)
    return serialized_tags
