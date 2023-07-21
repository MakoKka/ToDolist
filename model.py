import sqlite3 

class Task_list:
    def __init__(self, title,status):
        self.title = title
        self.status = status

    def save(self):
        connect = sqlite3.connect('taskslist.db')
        c = connect.cursor()
        c.execute("INSERT INTO taskslist (title, status) VALUES (?, ?)",
                  (self.title, self.status))
        connect.commit()
        connect.close()

    @staticmethod
    def get_all():
        connect = sqlite3.connect('taskslist.db')
        c = connect.cursor()
        c.execute("SELECT * FROM taskslist")
        rows = c.fetchall()
        connect.close()

        tasks = []
        for row in rows:
            task = Task_list(row[1], row[2])
            tasks.append(task)

        return tasks

    @staticmethod
    def mark_as_done(task_id):
        connect = sqlite3.connect('taskslist.db')
        c = connect.cursor()
        c.execute("UPDATE taskslist SET status='выполнена' WHERE id=?", (task_id,))
        connect.commit()
        connect.close()

    @staticmethod
    def delete(task_id):
        connect = sqlite3.connect('taskslist.db')
        c = connect.cursor()
        c.execute("DELETE FROM taskslist WHERE id=?", (task_id,))
        connect.commit()
        connect.close()