import sqlite3
import asyncio

# Это база данных пользователей (настройки времени и количества)
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
                words_quantity INTEGER
            )
        """)
        conn.commit()

def add_user(tg_id, nt, nq, wt, wq):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO users (tg_id, number_time, number_quantity, words_time, words_quantity)
            VALUES (?, ?, ?, ?, ?)
        """, (tg_id, nt, nq, wt, wq))
        conn.commit()

def find_user_id_by_tg_id(tg_id):
    """Находит внутренний ID пользователя по его VK ID (в коде оставили имя tg_id для совместимости)"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
        result = cursor.fetchone()
        return result[0] if result else None

def get_user_by_id(user_id):
    """Получает все настройки пользователя по его внутреннему ID"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

def changes_from_user(tg_id, field, value):
    """Обновляет настройки пользователя"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        allowed_fields = ['number_time', 'number_quantity', 'words_time', 'words_quantity']
        if field in allowed_fields:
            cursor.execute(f"UPDATE users SET {field} = ? WHERE tg_id = ?", (value, tg_id))
            conn.commit()