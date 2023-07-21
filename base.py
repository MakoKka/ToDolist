import sqlite3

# Создание таблицы для задач
def create_table():
    connect = sqlite3.connect('taskslist.db')
    c = connect.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS taskslist
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  status TEXT NOT NULL)''')
    connect.commit()
    connect.close()