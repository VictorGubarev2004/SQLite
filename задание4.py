!pip install peewee
from peewee import *
import datetime

# Подключаемся к базе данных SQLite
db = SqliteDatabase('university.db')

# Модели для таблиц
class BaseModel(Model):
    class Meta:
        database = db

class Student(BaseModel):
    name = CharField()
    surname = CharField()
    age = IntegerField()
    city = CharField()

class Course(BaseModel):
    name = CharField()
    time_start = DateField()
    time_end = DateField()

class StudentCourse(BaseModel):
    student = ForeignKeyField(Student, backref='courses')
    course = ForeignKeyField(Course, backref='students')

# Класс для работы с БД
class UniversityDB:
    def __init__(self):
        # Создаем таблицы, если они не существуют
        db.connect()
        db.create_tables([Student, Course, StudentCourse], safe=True)
        self.fill_initial_data_if_needed()

    def fill_initial_data_if_needed(self):
        if Student.select().count() == 0:
            self.fill_initial_data()

    def fill_initial_data(self):
        python_course = Course.create(name='python', time_start=datetime.date(2021, 7, 21), time_end=datetime.date(2021, 8, 21))
        java_course = Course.create(name='java', time_start=datetime.date(2021, 7, 13), time_end=datetime.date(2021, 8, 16))

        max = Student.create(name='Max', surname='Brooks', age=24, city='Spb')
        john = Student.create(name='John', surname='Stones', age=15, city='Spb')
        andy = Student.create(name='Andy', surname='Wings', age=45, city='Manchester')
        kate = Student.create(name='Kate', surname='Brooks', age=34, city='Spb')

        StudentCourse.create(student=max, course=python_course)
        StudentCourse.create(student=john, course=python_course)
        StudentCourse.create(student=andy, course=python_course)
        StudentCourse.create(student=kate, course=java_course)

    def get_students_over_30(self):
        return Student.select().where(Student.age > 30)

    def get_students_by_course(self, course_name):
        return (Student
                .select()
                .join(StudentCourse)
                .join(Course)
                .where(Course.name == course_name))

    def get_students_by_course_and_city(self, course_name, city):
        return (Student
                .select()
                .join(StudentCourse)
                .join(Course)
                .where((Course.name == course_name) & (Student.city == city)))

    def close(self):
        db.close()

def test_university_db():
    db = UniversityDB()
    
    print("Тест 1: Студенты старше 30 лет")
    students_over_30 = db.get_students_over_30()
    for student in students_over_30:
        print(f"{student.name} {student.surname}, Age: {student.age}, City: {student.city}")

    print("\nТест 2: Студенты, которые проходят курс по python")
    students_python = db.get_students_by_course('python')
    for student in students_python:
        print(f"{student.name} {student.surname}, Age: {student.age}, City: {student.city}")

    print("\nТест 3: Студенты, которые проходят курс по python и из Spb")
    students_python_spb = db.get_students_by_course_and_city('python', 'Spb')
    for student in students_python_spb:
        print(f"{student.name} {student.surname}, Age: {student.age}, City: {student.city}")
    
    db.close()

if __name__ == '__main__':
    test_university_db()