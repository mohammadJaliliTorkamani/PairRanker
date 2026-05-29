import os
import time
from contextlib import contextmanager

import mysql.connector
from mysql.connector import Error


MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "mysql"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "pairranker"),
    "password": os.getenv("MYSQL_PASSWORD", "pairranker_password"),
    "database": os.getenv("MYSQL_DATABASE", "pairranker_db"),
}


@contextmanager
def get_db():
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    try:
        yield connection
    finally:
        connection.close()


def initialize_database(max_retries: int = 30, retry_delay: float = 1.0):
    last_error = None

    for _ in range(max_retries):
        try:
            with get_db() as db:
                cursor = db.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS pairs (
                        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        user_id VARCHAR(255) NOT NULL,
                        left_text TEXT NOT NULL,
                        right_text TEXT NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_pairs_user_id (user_id)
                    )
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS responses (
                        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        user_id VARCHAR(255) NOT NULL,
                        pair_id VARCHAR(255) NOT NULL,
                        rating VARCHAR(50),
                        reason TEXT,
                        ground_truth TEXT,
                        prediction TEXT,
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_responses_user_id (user_id)
                    )
                    """
                )
                db.commit()
                cursor.close()
            return
        except Error as exc:
            last_error = exc
            time.sleep(retry_delay)

    raise RuntimeError("Could not initialize MySQL database") from last_error


def clear_survey_tables():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM pairs")
        cursor.execute("DELETE FROM responses")
        db.commit()
        cursor.close()


def replace_user_responses(user_id: str, responses: list[dict]):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM responses WHERE user_id = %s", (user_id,))

        if responses:
            cursor.executemany(
                """
                INSERT INTO responses (
                    user_id,
                    pair_id,
                    rating,
                    reason,
                    ground_truth,
                    prediction
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                [
                    (
                        response["user_id"],
                        response["pair_id"],
                        response["rating"],
                        response["reason"],
                        response.get("ground_truth"),
                        response.get("prediction"),
                    )
                    for response in responses
                ],
            )

        db.commit()
        cursor.close()


def insert_response(response: dict):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO responses (
                user_id,
                pair_id,
                rating,
                reason,
                ground_truth,
                prediction
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                response["user_id"],
                response["pair_id"],
                response.get("rating"),
                response.get("reason"),
                response.get("ground_truth"),
                response.get("prediction"),
            ),
        )
        db.commit()
        cursor.close()


def fetch_user_responses(user_id: str, limit: int = 10000):
    with get_db() as db:
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT user_id, pair_id, rating, reason, ground_truth, prediction
            FROM responses
            WHERE user_id = %s
            ORDER BY id
            LIMIT %s
            """,
            (user_id, limit),
        )
        responses = cursor.fetchall()
        cursor.close()
        return responses


def fetch_all_pairs(limit: int = 1000):
    with get_db() as db:
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, left_text, right_text
            FROM pairs
            ORDER BY id
            LIMIT %s
            """,
            (limit,),
        )
        pairs = cursor.fetchall()
        cursor.close()
        return pairs


def replace_user_pairs(user_id: str, pairs: list[dict]):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM pairs WHERE user_id = %s", (user_id,))

        if pairs:
            cursor.executemany(
                """
                INSERT INTO pairs (user_id, left_text, right_text)
                VALUES (%s, %s, %s)
                """,
                [
                    (pair["user_id"], pair["left"], pair["right"])
                    for pair in pairs
                ],
            )

        db.commit()
        cursor.close()
