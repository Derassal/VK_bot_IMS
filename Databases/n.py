import sqlite3
import re

def upload_texts():
    conn = sqlite3.connect('texts.db')
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS texts")
    cur.execute("""
        CREATE TABLE texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)

    try:
        with open('wow.txt', 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
            
        items = re.split(r'\n\s*\n', data)
        
        m = list()
        for i in items:
            t = i.strip()
            if len(t) > 10:
                m.append((t,))

        cur.executemany("INSERT INTO texts (content) VALUES (?)", m)
        conn.commit()
        
        print(f"Успех. Текстов загружено: {len(m)}")

    except FileNotFoundError:
        print("Ошибка: wow.txt не найден")
        
    finally:
        conn.close()

if __name__ == "__main__":
    upload_texts()