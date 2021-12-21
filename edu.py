import cmd
import mysql.connector
import pandas as pd
import uuid


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

    def do_add_course(self, arg):
        'add a course'

        course = input('Enter the course name: ')
        try:
            query = f'''insert into Courses values (uuid(), '{course}');'''
            # TODO: course number
            self.db.exec(query)
            self.db.commit()
            print('Done!')
        except mysql.connector.Error as error:
            print(
                f'Add a course failed with error: {error}')

    def do_add_course_offering(self, arg):
        'add a course offering'

        course = input('Enter the course name: ')
        offering = input('Enter the course offering name: ')
        term = input('Enter the term code: ')
        subject = input('Enter the subject: ')

        try:
            # TODO
            query = f''''''
            self.db.exec(query)
            self.db.commit()
            print('Done!')
        except mysql.connector.Error as error:
            print(
                f'Add a course offering failed with error: {error}')

    def do_add_grade_distribution(self, arg):
        'add a grade distribution'

        course_name = input('Enter the course offering name: ')
        section = input('Enter the section number: ')
        try:
            co_query = f'''
            select
                uuid
            from
                CourseOfferings
                where name = '{course_name}';
            '''
            ids = self.db.exec(co_query).fetchall()
            if not ids:
                print('No course found.')
                return
            co_id = ids[0][0]
            # TODO
        except mysql.connector.Error as error:
            print(f'Add a course grade failed with error: {error}')
        return

    # TODO: check
    def do_add_instructor(self, arg):
        'add an instructor'

        i_id = input('Enter the instructor id: ')
        name = input('Enter the instructor name: ')
        try:
            query = f'''insert into Instructors values ({i_id}, '{name}');'''
            self.db.exec(query)
            self.db.commit()
            print('Done!')
        except mysql.connector.Error as error:
            print(
                f'Add an instructor failed with error: {error}')

        # TODO: check ----- input code or name?
    def do_add_room(self, arg):
        'add a room'

        f_code = input('Enter the facility code: ')
        r_code = input('Enter the room code: ')
        try:
            query = f'''insert into Rooms values (uuid(),'{f_code}', '{r_code}');'''
            self.db.exec(query)
            self.db.commit()
            print('Done!')
        except mysql.connector.Error as error:
            print(
                f'Add an room failed with error: {error}')

    def do_find_course_location_and_time(self, arg):
        'find a course\'s location and time in this term'

        course_name = input('Enter the course name: ')
        section = input('Enter the section number: ')
        try:
            query = f'''
            select
                CO.name, S.number, R.facility_code, R.room_code, Sc.start_time, Sc.end_time,
                Sc.Monday, Sc.Tuesday, Sc.Wednesday, Sc.Thursday, Sc.Friday, Sc.Saturday, Sc.Sunday
            from
                CourseOfferings as CO
                inner join Sections AS S on CO.uuid = S.course_offering_uuid
                inner join Rooms as R on R.uuid = S.room_uuid
                inner join Schedules as Sc on Sc.uuid = S.schedule_uuid
                where CO.name = '{course_name}' and S.number = {section};
            '''
            raw_res = self.db.exec(query).fetchall()
            # data processing
            days = ['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday']
            res = []
            for e in raw_res:
                new_e = list(e[: 4])
                for i in range(4, 6):
                    new_e.append('{:02d}:{:02d}'.format(e[i]//60, e[i] % 60))
                for i in range(len(days)):
                    if e[6+i] == 1:
                        new_e.append(days[i])
                res.append(new_e)

            df = pd.DataFrame(
                res, columns=['course name', 'section number', 'facility code', 'room code', 'start time', 'end time', 'day'])
            print(df)
        except mysql.connector.Error as error:
            print(
                f'Find course\'s location and time failed with error: {error}')

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

    # TODO: check
    def do_get_section_grade(self, arg):
        'Get a section\'s grade distribution'

        course_name = input('Enter the course name: ')
        try:
            query = f'''
            select
                CO.name, G.section_number, a, ab, b, bc, d, f, s
            from
                CourseOfferings as CO
                inner join GradeDistributions as G on CO.uuid = G.course_offering_uuid
                where CO.name = '{course_name}';
            '''
            res = self.db.exec(query).fetchall()
            df = pd.DataFrame(
                res, columns=['name', 'section_number', 'a', 'ab', 'b', 'bc', 'd', 'f', 's'])
            print(df)
        except mysql.connector.Error as error:
            print(
                f'Get a section\'s grade distribution failed with error: {error}')\

    # TODO: check----not finish
    def do_get_section_rooms(self, arg):
        'Get a section\'s rooms'

        course_name = input('Enter the course name: ')
        section_number = input('Enter the section number: ')
        try:
            query = f'''
            select
                R.facility_code, R.room_code
            from
                CourseOfferings as CO
                inner join Sections as S on CO.uuid = S.course_offering_uuid
                inner join Rooms as R on S.room_uuid = R.id
                where CO.name = '{course_name}' and S.number = {section_number};
            '''
            res = self.db.exec(query).fetchall()
            df = pd.DataFrame(
                res, columns=['facility_code', 'R.room_code'])
            print(df)
        except mysql.connector.Error as error:
            print(
                f'Get a section\'s rooms failed with error: {error}')

    def do_q(self, args):
        'exit the program'

        return True


if __name__ == '__main__':
    Education().cmdloop()
