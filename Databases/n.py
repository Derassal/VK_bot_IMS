import sqlite3
import os


def dump_db(db_name: str):
    if not db_name.endswith(".db"):
        db_name += ".db"

    if not os.path.exists(db_name):
        print("❌ База не найдена")
        return

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    print(f"\n📦 DB: {db_name}\n" + "=" * 40)

    for (table,) in tables:
        print(f"\n📁 {table}")

        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        if not rows:
            print("   (пусто)")
            continue

        for i, row in enumerate(rows, 1):
            print(i, row)

    conn.close()


if __name__ == "__main__":
    name = input("DB name: ")
    dump_db(name)