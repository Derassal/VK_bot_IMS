import sqlite3

def is_database_empty(db_path: str) -> bool:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Вариант A: Проверяем, есть ли вообще таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    
    if not tables:
        conn.close()
        return True  # база пустая — нет таблиц
    
    # Вариант B: Проверяем, есть ли данные хотя бы в одной таблице
    for (table_name,) in tables:
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM [{table_name}] LIMIT 1);")
        has_data = cursor.fetchone()[0]
        if has_data:
            conn.close()
            return False  # база НЕ пустая
    
    conn.close()
    return True  # все таблицы пустые


# Пример использования
if is_database_empty('my_database.db'):
    print("База данных пустая")
else:
    print("В базе есть данные")