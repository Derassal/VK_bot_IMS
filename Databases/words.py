import sqlite3

def read_db():
    """Получает список слов для тренировки памяти"""
    try:
        with sqlite3.connect('Databases/words.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM words")
            return cursor.fetchall()
    except sqlit.Error:
        return []

def read_db2():
    """Получает тексты для упражнений по скорочтению"""
    try:
        with sqlite3.connect('Databases/texts.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM texts")
            return cursor.fetchall()
    except sqlite3.Error:
        return []