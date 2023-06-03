import sqlite3 as sql


def create_table():
    with sql.connect("bot.db") as con:
        con.execute("""CREATE TABLE IF NOT EXISTS languages(
            username TEXT,
            language_code TEXT
        )""")


def set_language(language_code: str, username: str):
    with sql.connect("bot.db") as con:
        cur = con.cursor()
        cur.execute(f"UPDATE languages SET language_code = '{language_code}' WHERE username = '{username}'")


def set_language_code(language_code: str, username: str):
    with sql.connect("bot.db") as con:
        cur = con.cursor()
        cur.execute(f"INSERT OR IGNORE INTO languages (username, language_code) VALUES ('{username}', '{language_code}')")


def get_language(username: str):
    with sql.connect("bot.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT language_code FROM languages WHERE username = '{username}'")
        language_code = cur.fetchone()[0]
        return language_code
