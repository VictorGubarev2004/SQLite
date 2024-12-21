import sqlite3

conn = sqlite3.connect('university.db')
cursor = conn.cursor()

cursor.executemany('''
INSERT INTO Courses (id, name, time_start, time_end)
VALUES (?, ?, ?, ?)
''', [
    (1, 'python', '2021-07-21', '2021-08-21'),
    (2, 'java', '2021-07-13', '2021-08-16')
])

cursor.executemany('''
INSERT INTO Students (id, name, surname, age, city)
VALUES (?, ?, ?, ?, ?)
''', [
    (1, 'Max', 'Brooks', 24, 'Spb'),
    (2, 'John', 'Stones', 15, 'Spb'),
    (3, 'Andy', 'Wings', 45, 'Manchester'),
    (4, 'Kate', 'Brooks', 34, 'Spb')
])

cursor.executemany('''
INSERT INTO Student_courses (student_id, course_id)
VALUES (?, ?)
''', [
    (1, 1),  # Max проходит курс python
    (2, 1),  # John проходит курс python
    (3, 1),  # Andy проходит курс python
    (4, 2)   # Kate проходит курс java
])

conn.commit()

cursor.execute('''
SELECT * FROM Students WHERE age > 30;
''')
print("Студенты старше 30 лет:")
for row in cursor.fetchall():
    print(row)

cursor.execute('''
SELECT Students.* 
FROM Students 
JOIN Student_courses ON Students.id = Student_courses.student_id
JOIN Courses ON Student_courses.course_id = Courses.id
WHERE Courses.name = 'python';
''')
print("\nСтуденты, которые проходят курс по python:")
for row in cursor.fetchall():
    print(row)

cursor.execute('''
SELECT Students.* 
FROM Students 
JOIN Student_courses ON Students.id = Student_courses.student_id
JOIN Courses ON Student_courses.course_id = Courses.id
WHERE Courses.name = 'python' AND Students.city = 'Spb';
''')
print("\nСтуденты, которые проходят курс по python и Spb:")
for row in cursor.fetchall():
    print(row)