import sqlite3
from config import DATABASE


class Database:

    def connect(self):
        con = sqlite3.connect(DATABASE)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def setup(self):
        with open("schema.sql", "r", encoding="utf-8") as file:
            schema = file.read()

        with self.connect() as con:
            con.executescript(schema)

    def get_user(self, discord_id):
        with self.connect() as con:
            return con.execute(
                "SELECT * FROM users WHERE discord_id = ?",
                (discord_id,)
            ).fetchone()

    def save_user(self, discord_id, username, budget, days, interests):
        with self.connect() as con:

            con.execute("""
                INSERT INTO users (discord_id, username, budget)
                VALUES (?, ?, ?)

                ON CONFLICT(discord_id)
                DO UPDATE SET
                    username = excluded.username,
                    budget = excluded.budget
            """, (discord_id, username, budget))

            user = con.execute(
                "SELECT * FROM users WHERE discord_id = ?",
                (discord_id,)
            ).fetchone()

            user_id = user["id"]

            con.execute(
                "DELETE FROM days WHERE user_id = ?",
                (user_id,)
            )

            con.execute(
                "DELETE FROM interests WHERE user_id = ?",
                (user_id,)
            )

            con.executemany(
                "INSERT INTO days (user_id, day) VALUES (?, ?)",
                [(user_id, day) for day in days]
            )

            con.executemany(
                "INSERT INTO interests (user_id, interest) VALUES (?, ?)",
                [(user_id, interest) for interest in interests]
            )

    def find_people(self, user_id, day, interest):
        with self.connect() as con:
            return con.execute("""
                SELECT DISTINCT users.*

                FROM users

                JOIN days
                    ON days.user_id = users.id

                JOIN interests
                    ON interests.user_id = users.id

                WHERE users.id != ?
                AND days.day = ?
                AND interests.interest = ?
            """, (user_id, day, interest)).fetchall()

    def find_group_activity(self, category, budget):
        with self.connect() as con:
            return con.execute("""
                SELECT *
                FROM activities

                WHERE category = ?
                AND price <= ?
                AND solo = 0

                ORDER BY RANDOM()
                LIMIT 1
            """, (category, budget)).fetchone()

    def find_solo(self, category, budget, limit=3):
        with self.connect() as con:
            return con.execute("""
                SELECT *
                FROM activities

                WHERE category = ?
                AND price <= ?
                AND solo = 1

                ORDER BY RANDOM()
                LIMIT ?
            """, (category, budget, limit)).fetchall()