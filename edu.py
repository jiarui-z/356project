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

    def do_check_course_offering(self, arg):
        return

    def do_get_course_offering_by_subject(self, arg):
        return

    def do_get_course_details(self, arg):
        'show the course\'s detail'

        course_name = input('Enter the course name: ')
        try:
            query = '''
            select
                distinct C.name, I.name, CO.term_code
            from
                Courses As C
                inner join CourseOfferings AS CO on C.uuid = CO.course_uuid
                inner join Sections AS S on CO.uuid = S.course_offering_uuid
                inner join Teachings AS T on S.uuid = T.section_uuid
                inner join Instructors AS I on T.instructor_id = I.id
                where C.name = '{}';
            '''.format(course_name)
            res = self.db.exec(query).fetchall()

            df = pd.DataFrame(
                res, columns=['course name', 'instructor name', 'term code'])
            print(df.to_string())
        except mysql.connector.Error as error:
            print('Get the course\'s detail failed with error: {}'.format(error))
            self.db.rollback()

    def do_show_all_instructors(self, arg):
        'show all instructors from UW Madison'

        try:
            query = 'select name from Instructors'
            res = self.db.exec(query).fetchall()
            df = pd.DataFrame(res, columns=['name'])
            print(df)
        except mysql.connector.Error as error:
            print('Get all instructors failed with error: {}'.format(error))


if __name__ == '__main__':
    Education().cmdloop()
