# Education
This project uses MySQL and the data from Kaggle to explore the course related information from the University of Wisconsin and Coursera

## Project Structures
**ER_Diagram.pdf** contains our ER diagram for our database tables.
**project.sql** contains the SQL commands to set up the database.
**edu.py** contains our CLI application.

## Prerequisites
- `Python3`
- `MySQL8.0`
- `mysql-connector`
- `pandas`

## Installation
Run the following command to install all the dependencies.
```pip3 install pandas mysql-connector-python```

## Getting Started
After installing all the dependencies, we can now start our education application.
```python
python3 edu.py
```
This will connect to our own database on the marmoset (Please connect to the campus's VPN).

## Usage
You can use `?` or `help` to show all available commands.
- `add_course`
    - users can use this command to add a course to the University of Madison or Coursera

### University of Madison
- `add_course_offering`
    - users can use this command to add a course offering

- `add_grade_distribution`
    - users can use this command to add grades to a course offering section

- `add_instructor`
    - users can use this command to add an instructor

- `add_room`
    - users can use this command to

- `check_course_offering`
    - users can use this command to add a course offering

- `find_course_location_and_time`
    - users can use this command to find a course offering's sections, room and time slots

- `get_course_instructors`
    - users can use this command to find who teaches this course in which term

- `get_course_offering_by_subject`
    - users can use this command to get all the courses under a subject

- `get_section_grade`
    - users can use this command to get a section's grade distribution

- `show_all_instructors`
    - users can use this command to list all instructors

- `get_section_rooms`
    - users can use this command to 

### Coursera
- `add_review`
    - users can use this command to add a review

- `get_course_reviews`
    - users can use this command to get all reviews of a course
    - users can filter the reviews by rating

## Error Handling
All commands catch MySQL error and miising input error. In the case when multiple SQL queries are used to update the database, the operations will not be committed if there is an error in any of the queries to ensure atomicity.