import cmd
import mysql.connector
import pandas as pd


class DB:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='marmoset04.shoshin.uwaterloo.ca',
            user='h93zheng',
            password='dblW65zwrxUfMg3OHR%4',
            database='db356_h93zheng'
        )
        self.cursor = self.connection.cursor()

    def exec(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()


class Education(cmd.Cmd):
    intro = 'Type help to show all available commands.\nType q to exit the program.\n'
    prompt = '(edu) '

    def __init__(self):
        super(Education, self).__init__()
        self.db = DB()

    def do_check_course_offering(self, arg):
        'check if a course is offered in a term'

        course_name = input('Enter the course name: ')
        term = input('Enter the term code: ')
        try:
            query = f'''
            select
                count(1)
            from
                Courses As C
                inner join CourseOfferings AS CO on C.uuid = CO.course_uuid
                where C.name = '{course_name}' and CO.term_code = '{term}';
            '''
            res = self.db.exec(query).fetchall()[0][0]
            if res:
                print(f'{course_name} is offered in {term}')
            else:
                print(f'{course_name} is not offered in {term}')
        except mysql.connector.Error as error:
            print(f'Check course offering failed with error: {error}')

    def do_get_course_offering_by_subject(self, arg):
        'get all course offerings in a subject'

        subject = input('Enter the subject code: ')

        try:
            query = f'''
            select
                distinct CO.name
            from
                Subjects As S
                inner join SubjectMemberships AS SM on S.code = SM.subject_code
                inner join CourseOfferings AS CO on SM.course_offering_uuid = CO.uuid
                where S.code = {subject};
            '''
            res = self.db.exec(query).fetchall()

            df = pd.DataFrame(
                res, columns=['course offering name'])
            print(df)
        except mysql.connector.Error as error:
            print(
                f'Get course offerings by subject failed with error: {error}')
        return

    def do_get_course_details(self, arg):
        'show a course\'s detail'

        course_name = input('Enter the course name: ')
        try:
            query = f'''
            select
                distinct C.name, I.name, CO.term_code
            from
                Courses As C
                inner join CourseOfferings AS CO on C.uuid = CO.course_uuid
                inner join Sections AS S on CO.uuid = S.course_offering_uuid
                inner join Teachings AS T on S.uuid = T.section_uuid
                inner join Instructors AS I on T.instructor_id = I.id
                where C.name = '{course_name}';
            '''
            res = self.db.exec(query).fetchall()

            df = pd.DataFrame(
                res, columns=['course name', 'instructor name', 'term code'])
            print(df)
        except mysql.connector.Error as error:
            print(f'Get the course\'s detail failed with error: {error}')

    def do_show_all_instructors(self, arg):
        'show all instructors from UW Madison'

        try:
            query = 'select name from Instructors'
            res = self.db.exec(query).fetchall()
            df = pd.DataFrame(res, columns=['name'])
            print(df)
        except mysql.connector.Error as error:
            print(f'Get all instructors failed with error: {error}')

    def do_q(self, args):
        'exit the program'

        return True


if __name__ == '__main__':
    Education().cmdloop()
