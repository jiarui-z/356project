import mysql.connector


def connect():
    db = mysql.connector.connect(
        host="marmoset04.shoshin.uwaterloo.ca",
        user="j879zhan",
        password="Zhangjr12."
    )
    return db


if __name__ == "__main__":
    # how to use it
    db = connect()
    c = db.cursor(buffered=True)
    c.execute('show databases;')
    print(c.fetchall())
