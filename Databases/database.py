import sqlite3

DB_PATH = 'Databases/db.db'

def create_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER UNIQUE,
                number_time INTEGER,
                number_quantity INTEGER,
                words_time INTEGER,
                words_quantity INTEGER,
                lang_pair TEXT DEFAULT 'rus rus'
            )
        """)
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN lang_pair TEXT DEFAULT 'rus rus'")
        except:
            pass
        conn.commit()

def add_user(tg_id, nt, nq, wt, wq):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO users (tg_id, number_time, number_quantity, words_time, words_quantity, lang_pair)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tg_id, nt, nq, wt, wq, 'rus rus'))
        conn.commit()

def find_user_id_by_tg_id(tg_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
        result = cursor.fetchone()
        return result[0] if result else None

def get_user_by_id(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

def get_user_lang(tg_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT lang_pair FROM users WHERE tg_id = ?", (tg_id,))
        res = cursor.fetchone()
        return res[0] if res else 'rus rus'

def changes_from_user(tg_id, field, value):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        allowed = ['number_time', 'number_quantity', 'words_time', 'words_quantity', 'lang_pair']
        if field in allowed:
            cursor.execute(f"UPDATE users SET {field} = ? WHERE tg_id = ?", (value, tg_id))
            conn.commit()