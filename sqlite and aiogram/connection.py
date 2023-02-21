import sqlite3


def create_db():
    db = sqlite3.connect('main.db')
    sql = db.cursor()
    sql.execute('''CREATE TABLE IF NOT EXISTS user_info(
    user_id BIGINT PRIMARY KEY, 
    first_name VARCHAR )''')
    db.commit()
    sql.close()
    db.close()


def database_query(query: str, arg):
    db = sqlite3.connect('main.db', check_same_thread=False)
    with db:
        sql = db.cursor()
        sql.execute(query, arg)
        result = sql.fetchall()
        return result

    if db:
        db.commit()
        sql.close()
        db.close()


def send_users(query: str):
    db = sqlite3.connect('main.db', check_same_thread=False)
    with db:
        sql = db.cursor()
        sql.execute(query)
        result = sql.fetchall()

    if db:
        db.commit()
        sql.close()

    return result
