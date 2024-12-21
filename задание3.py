import sqlite3

class University:
    def __init__(self, db_name='university.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.create_connection()

    def create_connection(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            time_start TEXT NOT NULL,
            time_end TEXT NOT NULL
        );
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            age INTEGER,
            city TEXT
        );
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student_courses (
            student_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES Students(id),
            FOREIGN KEY (course_id) REFERENCES Courses(id),
            PRIMARY KEY (student_id, course_id)
        );
        ''')

        # Проверка данных
        self.cursor.execute("SELECT COUNT(*) FROM Students")
        student_count = self.cursor.fetchone()[0]
        if student_count == 0:
            self.fill_initial_data()

    def fill_initial_data(self):
       
        self.cursor.executemany('''
        INSERT INTO Courses (name, time_start, time_end)
        VALUES (?, ?, ?)
        ''', [
            ('python', '2021-07-21', '2021-08-21'),
            ('java', '2021-07-13', '2021-08-16')
        ])

        self.cursor.executemany('''
        INSERT INTO Students (name, surname, age, city)
        VALUES (?, ?, ?, ?)
        ''', [
            ('Max', 'Brooks', 24, 'Spb'),
            ('John', 'Stones', 15, 'Spb'),
            ('Andy', 'Wings', 45, 'Manchester'),
            ('Kate', 'Brooks', 34, 'Spb')
        ])

        # Вставка данных в таблицу Student_courses
        self.cursor.executemany('''
        INSERT INTO Student_courses (student_id, course_id)
        VALUES (?, ?)
        ''', [
            (1, 1),  
            (2, 1),  
            (3, 1),  
            (4, 2)   
        ])

        self.conn.commit()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_students_over_30(self):
        return self.execute_query('''
        SELECT * FROM Students WHERE age > 30;
        ''')

    def get_students_by_course(self, course_name):
        return self.execute_query('''
        SELECT Students.* 
        FROM Students 
        JOIN Student_courses ON Students.id = Student_courses.student_id
        JOIN Courses ON Student_courses.course_id = Courses.id
        WHERE Courses.name = ?;
        ''', (course_name,))

    def get_students_by_course_and_city(self, course_name, city):
        return self.execute_query('''
        SELECT Students.* 
        FROM Students 
        JOIN Student_courses ON Students.id = Student_courses.student_id
        JOIN Courses ON Student_courses.course_id = Courses.id
        WHERE Courses.name = ? AND Students.city = ?;
        ''', (course_name, city))

# Тест
def test_university():
    db = University()
    print("Тест 1: Студенты старше 30 лет")
    students_over_30 = db.get_students_over_30()
    for student in students_over_30:
        print(student)

    print("\nТест 2: Студенты, которые проходят курс по python")
    students_python = db.get_students_by_course('python')
    for student in students_python:
        print(student)

    print("\nТест 3: Студенты, которые проходят курс по python и Spb")
    students_python_spb = db.get_students_by_course_and_city('python', 'Spb')
    for student in students_python_spb:
        print(student)
    
    db.close_connection()

if __name__ == '__