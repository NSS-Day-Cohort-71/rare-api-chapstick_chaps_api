import sqlite3
import json
from datetime import datetime

def create_comment(comment):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Comments (post_id, author_id, content, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                comment["post_id"],
                comment["author_id"],
                comment["content"],
                datetime.now(),
            ),
        )

        id = db_cursor.lastrowid
        return json.dumps({"comment_id": id})

def get_comments():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT 
                c.id,
                c.post_id,
                c.author_id,
                u.username as author,
                c.content,
                c.created_at
            FROM Comments c
            LEFT JOIN Users u ON c.author_id = u.id
        """
        )

        query_results = db_cursor.fetchall()
        comments = []
        for row in query_results:
            comment = {
                "id": row["id"],
                "post_id": row["post_id"],
                "author_id": row["author_id"],
                "author": row["author"],
                "content": row["content"],
                "created_at": row["created_at"],
            }
            comments.append(comment)

        return json.dumps(comments)
