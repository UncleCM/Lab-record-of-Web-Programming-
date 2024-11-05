import transaction
from ZODB import FileStorage, DB
from persistent import Persistent
from persistent.list import PersistentList
from BTrees._OOBTree import OOBTree


class Course(Persistent):
    def __init__(self, credit, course_id, name, grade_scheme=None):
        super().__init__()
        self.credit = credit
        self.id = course_id
        self.name = name
        self.grade_scheme = grade_scheme if grade_scheme is not None else []

    def get_credit(self):
        return self.credit

    def set_name(self, name):
        self.name = name

    def score_grading(self, score):
        return f"ID: {self.id} Name: {self.name} Credit: {self.credit}"

    def set_grade_scheme(self, scheme):
        self.grade_scheme = scheme

    def print_detail(self):
        print(f"ID:\t{self.id} Course: {self.name}\t, Credit: {self.credit}")


class Enrollment(Persistent):
    def __init__(self, course, student, score=0):
        super().__init__()
        self.course = course
        self.student = student
        self.score = score

    def get_course(self):
        return self.course

    def get_grade(self):
        for grade in self.course.grade_scheme:
            if grade['min'] <= self.score <= grade['max']:
                return grade['Grade']
        return None

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def print_detail(self):
        print(f"\tID:\t{self.course.id} Course: {self.course.name}\t, Credit: {self.course.credit} Score:  {int(self.score)} Grade: {self.get_grade()}")


class Student(Persistent):
    def __init__(self, student_id, name=""):
        super().__init__()
        self.enrollments = PersistentList()
        self.id = student_id
        self.name = name

    def enroll_course(self, course, score=0):
        enrollment = Enrollment(course, self, score)
        self.enrollments.append(enrollment)
        return enrollment

    def get_enrollment(self, course):
        for enrollment in self.enrollments:
            if enrollment.get_course() == course:
                return enrollment
        return None

    def print_transcript(self):
        total_credits = 0
        total_grade_points = 0.0
        print(f"\tTranscript\nID:\t{self.id}  Name: {self.name}\nCourse list")
        for enrollment in self.enrollments:
            course = enrollment.get_course()
            grade = enrollment.get_grade()
            enrollment.print_detail()
            if grade is not None:
                total_credits += course.get_credit()
                grade_points = {
                    "A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0
                }.get(grade, 0.0)
                total_grade_points += grade_points * course.get_credit()

        if total_credits > 0:
            gpa = total_grade_points / total_credits
            print(f"Total GPA is: {gpa:.2f}\n")
        else:
            print("No grades available to calculate GPA.\n")

    def set_name(self, name):
        self.name = name


storage = FileStorage.FileStorage('students_data.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

if 'courses' not in root:
    root['courses'] = OOBTree()

if 'students' not in root:
    root['students'] = OOBTree()

grading = [
    {"Grade": "A", "min": 80, "max": 100},
    {"Grade": "B", "min": 70, "max": 79},
    {"Grade": "C", "min": 60, "max": 69},
    {"Grade": "D", "min": 50, "max": 59},
    {"Grade": "F", "min": 0, "max": 49},
]

def test_case():
    course1 = Course(4, "101", "Computer Programming", grading)
    course2 = Course(4, "201", "Web Programming", grading)
    course3 = Course(5, "202", "Software Engineering Principle", grading)
    course4 = Course(3, "301", "Artificial Intelligence", grading)

    root.courses = OOBTree()
    root.courses[101] = course1
    root.courses[201] = course2
    root.courses[202] = course3
    root.courses[301] = course4

    student1 = Student(student_id=1101, name="Mr. Christian de Neuvillette")
    student2 = Student(student_id=1102, name="Mr. Zhong Li")
    student3 = Student(student_id=1103, name="Mr. Dvalinn Durinson")


    root['students'][1101] = student1
    root['students'][1102] = student2
    root['students'][1103] = student3

    student1.enroll_course(course1, 85.0)
    student1.enroll_course(course2, 73.0)
    student1.enroll_course(course4, 60.0)

    student2.enroll_course(course1, 90.0)
    student2.enroll_course(course2, 78.0)
    student2.enroll_course(course3, 67.0)

    student3.enroll_course(course1, 55.0)
    student3.enroll_course(course2, 80.0)
    student3.enroll_course(course3, 45.0)
    student3.enroll_course(course4, 89.0)

    transaction.commit()

    retrieved_course1 = root.courses[101]
    retrieved_course2 = root.courses[201]
    retrieved_course3 = root.courses[202]
    retrieved_course4 = root.courses[301]

    retrieved_course1.print_detail()
    retrieved_course2.print_detail()
    retrieved_course3.print_detail()
    retrieved_course4.print_detail()
    print("")

    for student_id in root['students']:
        retrieved_student = root['students'][student_id]
        retrieved_student.print_transcript()


test_case()

transaction.commit()
connection.close()
db.close()
