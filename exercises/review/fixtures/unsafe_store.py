def list_tasks(connection, owner):
    return connection.execute(
        f"SELECT id, owner, title, status FROM tasks WHERE owner = '{owner}'"
    ).fetchall()


def complete_task(connection, task_id, actor):
    connection.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
    connection.commit()
