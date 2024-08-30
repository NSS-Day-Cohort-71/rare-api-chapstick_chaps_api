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


def get_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT 
                p.id,
                p.user_id,
                u.id as userId,
                u.username as username,
                p.category_id,
                c.id as categoryId,
                c.label as categoryLabel,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved
            FROM Posts p
            LEFT JOIN Categories c ON p.category_id = c.id
            LEFT JOIN Users u ON p.user_id = u.id 
        """
        )

        query_results = db_cursor.fetchall()
        posts = []
        for row in query_results:
            category = (
                {
                    "id": row["categoryId"],
                    "label": row["categoryLabel"],
                }
                if row["categoryId"]
                else {
                    "id": None,
                    "label": "no category available",
                }
            )
            user = {"id": row["userId"], "username": row["username"]}
            post = {
                "id": row["id"],
                "user_id": row["userId"],
                "category_id": row["categoryId"],
                "title": row["title"],
                "publication_date": row["publication_date"],
                "image_url": row["image_url"],
                "content": row["content"],
                "approved": row["approved"],
                "category": category,
                "user": user,
            }
            posts.append(post)

        serialized_posts = json.dumps(posts)
    return serialized_posts


def get_posts_by_user_id(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
                SELECT
                    p.id,
                    p.user_id,
                    u.id as userId,
                    u.username as username,
                    p.category_id,
                    c.id as categoryId,
                    c.label as categoryLabel,
                    p.title,
                    p.publication_date,
                    p.image_url,
                    p.content,
                    p.approved
            FROM Posts p
            LEFT JOIN Categories c ON p.category_id = c.id
            LEFT JOIN Users u ON p.user_id = u.id
            WHERE p.user_id = ?
            """,
            (id,),
        )
        query_results = db_cursor.fetchall()
        posts = []
        for row in query_results:
            category = (
                {
                    "id": row["categoryId"],
                    "label": row["categoryLabel"],
                }
                if row["categoryId"]
                else {
                    "id": None,
                    "label": "no category available",
                }
            )
            user = {"id": row["userId"], "username": row["username"]}
            post = {
                "id": row["id"],
                "user_id": row["userId"],
                "user": user,
                "category_id": row["categoryId"],
                "category": category,
                "title": row["title"],
                "publication_date": row["publication_date"],
                "image_url": row["image_url"],
                "content": row["content"],
                "approved": row["approved"],
            }
            posts.append(post)

        serialized_posts = json.dumps(posts)
    return serialized_posts


def get_postById(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT 
                p.id,
                p.user_id,
                u.id as userId,
                u.username as username,
                p.category_id,
                c.id as categoryId,
                c.label as categoryLabel,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved
            FROM Posts p
            LEFT JOIN Categories c ON p.category_id = c.id
            LEFT JOIN Users u ON p.user_id = u.id 
            WHERE p.id = ?
            """,
            (pk,),
        )

        row = db_cursor.fetchone()
        if row:
            category = (
                {
                    "id": row["categoryId"],
                    "label": row["categoryLabel"],
                }
                if row["categoryId"]
                else {
                    "id": None,
                    "label": "no category available",
                }
            )
            user = {"id": row["userId"], "username": row["username"]}
            post = {
                "id": row["id"],
                "user_id": row["userId"],
                "category_id": row["categoryId"],
                "title": row["title"],
                "publication_date": row["publication_date"],
                "image_url": row["image_url"],
                "content": row["content"],
                "approved": row["approved"],
                "category": category,
                "user": user,
            }
            serialized_post = json.dumps(post)
            return serialized_post
        else:
            return None
