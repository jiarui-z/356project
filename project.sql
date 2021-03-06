-- Courses
create table Courses (
        uuid char(36) primary key, 
        name varchar(150) not null
);

load data infile '/var/lib/mysql-files/26-Education/UWM/courses.csv' ignore into table Courses
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (@col1, @col2, @col3)
    set uuid = @col1, name = @col2;

create index course_name_idx on Courses(name);

create table MadisonCourses (
    uuid char(36) primary key,
    number int not null check (number > 0),
    
    foreign key (uuid) references Courses(uuid)
);

load data infile '/var/lib/mysql-files/26-Education/UWM/courses.csv' ignore into table MadisonCourses
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (@col1, @col2, @col3)
    set uuid = @col1, number = @col3;

-- CourseOfferings
create table CourseOfferings (
        uuid char(36) primary key, 
        course_uuid char(36) not null,
        term_code int not null check(term_code > 1013 and term_code < 1513),
        name varchar(30) not null,

        foreign key (course_uuid) references Courses(uuid)
);

load data infile '/var/lib/mysql-files/26-Education/UWM/course_offerings.csv' ignore into table CourseOfferings
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines;

create index course_offerings_name_idx on CourseOfferings(name);
create index course_offerings_cu_idx on CourseOfferings(course_uuid);
create index course_offerings_tc_idx on CourseOfferings(term_code);

--CourseraCourses
create table CourseraCourses(
    name varchar(150) not null,
    institution varchar(70) not null,
    course_url varchar(120) not null,
    course_id varchar(100),
    uuid char(36)
);

load data infile '/var/lib/mysql-files/26-Education/Coursera/Coursera_courses.csv' ignore into table CourseraCourses
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines;

update CourseraCourses set uuid=uuid();

create index coursera_courses_url_idx on CourseraCourses(course_url);

-- CourseraReviews
create table CourseraReviews(
    reviews varchar(1000),
    reviewers varchar(100),
    date_reviews char(12),
    rating int,
    course_id varchar(100)
    course_uuid char(36)
);

load data infile '/var/lib/mysql-files/26-Education/Coursera/Coursera_reviews.csv' ignore into table CourseraReviews
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines;

update CourseraReviews inner join CourseraCourses 
    on (CourseraReviews.course_id = CourseraCourses.course_id) 
    set CourseraReviews.course_uuid = CourseraCourses.uuid;

alter table CourseraReviews add uuid char(36);
update CourseraReviews set uuid=uuid();
alter table CourseraReviews add primary key (uuid);

alter table CourseraReviews drop course_id;
alter table CourseraCourses drop course_id;
alter table CourseraCourses add primary key (uuid);
alter table CourseraReviews add foreign key (course_uuid) references CourseraCourses(uuid);
alter table CourseraCourses add foreign key (uuid) references Courses(uuid);

insert into Courses (uuid, name)???select uuid, name from CourseraCourses;

alter table CourseraCourses drop column name;

create index coursera_review_cu_idx on CourseraReviews(course_uuid);

-- Instructors
create table Instructors (
        id int primary key,
        name varchar(50) not null
);

load data infile '/var/lib/mysql-files/26-Education/UWM/instructors.csv' ignore into table Instructors
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines;

create index instructors_idx on Instructors(name);

-- Rooms
create table Rooms (
        uuid char(36) primary key,
        facility_code varchar(10) not null,
        room_code char(5) 
);

load data infile '/var/lib/mysql-files/26-Education/UWM/rooms.csv' ignore into table Rooms
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines;

-- Schedules
create table Schedules (
        uuid char(36) primary key,
        start_time int not null,
        end_time int not null,
        Monday char(1) not null check (Monday IN ('t','f')),
        Tuesday char(1) not null check (Tuesday IN ('t','f')),
        Wednesday char(1) not null check (Wednesday IN ('t','f')),
        Thursday char(1) not null check (Thursday IN ('t','f')),
        Friday char(1) not null check (Friday IN ('t','f')),
        Saturday char(1) not null check (Saturday IN ('t','f')),
        Sunday char(1) not null check (Sunday IN ('t','f'))
);

load data infile '/var/lib/mysql-files/26-Education/UWM/schedules.csv' ignore into table Schedules
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines;

-- Subjects
create table Subjects (
        code int primary key check(code > 0),
        name varchar(50) not null,
        abbreviation varchar(10) not null
);

load data infile '/var/lib/mysql-files/26-Education/UWM/subjects.csv' ignore into table Subjects
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines;

-- Subject_memberships
create table SubjectMemberships (
        subject_code int not null check(subject_code > 0),
        course_offering_uuid char(36) not null,

        primary key (subject_code, course_offering_uuid),
        foreign key (subject_code) references Subjects(code),
        foreign key (course_offering_uuid) references CourseOfferings(uuid)
);

load data infile '/var/lib/mysql-files/26-Education/UWM/subject_memberships.csv' ignore into table SubjectMemberships
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines;

create index subject_memberships_cou_idx on SubjectMemberships(course_offering_uuid);

-- Sections
create table Sections(
        uuid char(36) primary key,
        course_offering_uuid char(36) not null,
        section_type char(3) not null,
        number int not null check (number > 0),
        room_uuid char(36),
        schedule_uuid char(36),
        
        foreign key (course_offering_uuid) references CourseOfferings(uuid),
        foreign key (room_uuid) references Rooms(uuid),
        foreign key (schedule_uuid) references Schedules(uuid)
);

load data infile '/var/lib/mysql-files/26-Education/UWM/sections.csv' ignore into table Sections
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines;

create index sections_comp_idx on Sections(course_offering_uuid, room_uuid, schedule_uuid);
create index sections_num_idx on Sections(number);

-- Teachings
create table Teachings (
        instructor_id int not null check(instructor_id > 0),
        section_uuid char(36) not null,

        primary key (instructor_id, section_uuid),
        foreign key (instructor_id) references Instructors(id),
        foreign key (section_uuid) references Sections(uuid)
);

load data infile '/var/lib/mysql-files/26-Education/UWM/teachings.csv' ignore into table Teachings 
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines;

create index teachings_su_idx on Teachings(section_uuid);

-- GradeDistributions
create table GradeDistributions (
        course_offering_uuid char(36),
        section_number int not null check (section_number > 0),
        a int not null check (a >= 0),
        ab int not null check (ab >= 0),
        b int not null check (b >= 0),
        bc int not null check (bc >= 0),
        c int not null check (c >= 0),
        d int not null check (d >= 0),
        f int not null check (f >= 0),
        s int not null check (s >= 0),

        primary key (course_offering_uuid, section_number),
        foreign key (course_offering_uuid) references CourseOfferings(uuid),
        foreign key (section_number) references Sections(number)
);

load data infile '/var/lib/mysql-files/26-Education/UWM/grade_distributions.csv' ignore into table GradeDistributions
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines;