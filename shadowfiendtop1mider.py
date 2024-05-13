import sqlite3

with sqlite3.connect("sliv.db") as db:
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS id_tg (
        id INTEGER PRIMARY KEY
    )""")
    db.commit()


def add_id(id_user):
    with sqlite3.connect("sliv.db") as db:
        db = sqlite3.connect("sliv.db")
        c = db.cursor()
        c.execute("SELECT id FROM id_tg WHERE rowid = ?", (id_user,))
        if c.fetchone() is None:
            c.execute("INSERT INTO id_tg(id) VALUES(?)", (id_user,))
            db.commit()
