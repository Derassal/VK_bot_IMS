import sqlite3

def create_spanish_db():
    conn = sqlite3.connect("spanish_words.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT
    )
    """)

    with open("spanish_words.txt", "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]

    cur.executemany("INSERT INTO words (word) VALUES (?)", [(w,) for w in words])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_spanish_db()