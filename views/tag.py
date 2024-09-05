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
            ORDER BY t.label
        """
        )

        query_results = db_cursor.fetchall()
        tags = []
        for row in query_results:
            tags.append(dict(row))

        serialized_tags = json.dumps(tags)
    return serialized_tags


def create_tag(tag):

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
                INSERT INTO Tags (label)
                VALUES (?)
            """,
            (tag["label"],),
        )

        id = db_cursor.lastrowid

        return json.dumps({"tag_id": id})


def update_tag(pk, tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
                UPDATE Tags
                    SET
                        label = ?
                WHERE id = ?
            """,
            (
                tag["label"],
                pk,
            ),
        )
        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False
