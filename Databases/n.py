import sqlite3
import re
import os

path = 'Databases/words.db'

if not os.path.exists('Databases'):
    os.makedirs('Databases')

conn = sqlite3.connect(path)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS words")
cur.execute("CREATE TABLE words (word TEXT)")

try:
    with open('wow.txt', 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read().lower()
    
    items = re.findall(r'[а-яё]+', data)
    uniq = set(items)
    
    m = list()
    for w in uniq:
        if len(w) > 1:
            m.append((w,))
            
    cur.executemany("INSERT INTO words (word) VALUES (?)", m)
    conn.commit()
    
    count = len(m)
    print(f"Загружено слов: {count}")

except FileNotFoundError:
    print("Файл wow.txt не найден")

finally:
    conn.close()