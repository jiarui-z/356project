import cmd
import mysql.connector
import pandas as pd


class DB:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='marmoset04.shoshin.uwaterloo.ca',
            user='h93zheng',
            password='dblW65zwrxUfMg3OHR%4'
        )
        self.cursor = self.connection.cursor()
        self.exec('use db356_h93zheng')

    def exec(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()


class Education(cmd.Cmd):
    intro = 'Type help to show all available commands.\n'
    prompt = '(edu) '

    def __init__(self):
        super(Education, self).__init__()
        self.db = DB()

    def do_get_all_instructors(self, arg):
        try:
            query = 'select name from Instructors'
            res = self.db.exec(query).fetchall()

            df = pd.DataFrame(res, columns=['name'])
            print(df)
        except mysql.connector.Error as error:
            print('Get all instructors failed with error: {}'.format(error))
            self.db.rollback()


if __name__ == '__main__':
    Education().cmdloop()
