import sqlite3
import json
from datetime import datetime


def create_post(post):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        Insert into Posts (user_id, category_id, title, publication_date, image_url, content, approved) values (?, ?, ?, ?, ?, ?, 1)
        """,
            (
                post["userId"],
                post["categoryId"],
                post["title"],
                datetime.now(),
                post["imageUrl"],
                post["content"],
            ),
        )

        id = db_cursor.lastrowid

        return json.dumps({"post_id": id})
