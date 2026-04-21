```python
import sqlite3

def is_database_empty(db_path: str) -> bool:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    
    if not tables:
        conn.close()
        return True
    
    for (table_name,) in tables:
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM [{table_name}] LIMIT 1);")
        has_data = cursor.fetchone()[0]
        if has_data:
            conn.close()
            return False
    
    conn.close()
    return True

if is_database_empty('my_database.db'):
    print("База данных пустая")
else:
    print("В базе есть данные")
```
