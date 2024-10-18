import transaction
from model import Course, Student
from main import root, close_connection  # Import root and close_connection from main.py

if __name__ == "__main__":
    # Adding courses with grade schemes
    if 101 not in root.courses:
        root.courses[101] = Course(101, "Computer Programming", 4)
        root.courses[101].setGradeScheme(
            [
                {"min_score": 80, "max_score": 100, "grade": "A"},
                {"min_score": 70, "max_score": 79, "grade": "B"},
                {"min_score": 60, "max_score": 69, "grade": "C"},
                {"min_score": 50, "max_score": 59, "grade": "D"},
                {"min_score": 0, "max_score": 49, "grade": "F"},
            ]
        )

    if 201 not in root.courses:
        root.courses[201] = Course(201, "Web Programming", 4)
        root.courses[201].setGradeScheme(
            [
                {"min_score": 80, "max_score": 100, "grade": "A"},
                {"min_score": 70, "max_score": 79, "grade": "B"},
                {"min_score": 60, "max_score": 69, "grade": "C"},
                {"min_score": 50, "max_score": 59, "grade": "D"},
                {"min_score": 0, "max_score": 49, "grade": "F"},
            ]
        )

    if 202 not in root.courses:
        root.courses[202] = Course(202, "Software Engineering Principles", 5)
        root.courses[202].setGradeScheme(
            [
                {"min_score": 80, "max_score": 100, "grade": "A"},
                {"min_score": 70, "max_score": 79, "grade": "B"},
                {"min_score": 60, "max_score": 69, "grade": "C"},
                {"min_score": 50, "max_score": 59, "grade": "D"},
                {"min_score": 0, "max_score": 49, "grade": "F"},
            ]
        )

    if 301 not in root.courses:
        root.courses[301] = Course(301, "Artificial Intelligence", 3)
        root.courses[301].setGradeScheme(
            [
                {"min_score": 80, "max_score": 100, "grade": "A"},
                {"min_score": 70, "max_score": 79, "grade": "B"},
                {"min_score": 60, "max_score": 69, "grade": "C"},
                {"min_score": 50, "max_score": 59, "grade": "D"},
                {"min_score": 0, "max_score": 49, "grade": "F"},
            ]
        )

    # Adding students
    if 1101 not in root.students:
        root.students[1101] = Student(1101, "Mr. Christian de Neuvillette")
    if 1102 not in root.students:
        root.students[1102] = Student(1102, "Mr. Zhong Li")
    if 1103 not in root.students:
        root.students[1103] = Student(1103, "Mr. Dvalinn Durinson")

    # Enroll students and set scores
    student1 = root.students[1101]
    if not student1.enrolls:
        student1.enroll_course(root.courses[101], 85)
        student1.enroll_course(root.courses[201], 88)
        student1.enroll_course(root.courses[301], 72)

    student2 = root.students[1102]
    if not student2.enrolls:
        student2.enroll_course(root.courses[101], 92)
        student2.enroll_course(root.courses[201], 81)
        student2.enroll_course(root.courses[202], 60)

    student3 = root.students[1103]
    if not student3.enrolls:
        student3.enroll_course(root.courses[101], 75)
        student3.enroll_course(root.courses[201], 95)
        student3.enroll_course(root.courses[202], 85)
        student3.enroll_course(root.courses[301], 65)

    # Commit the transaction
    transaction.commit()

    # Printing course details
    print("================ RESTART: pythoncode ================")
    for course in root.courses.values():
        if isinstance(course, Course):
            course.print_detail()
        else:
            print("Not a Course object:", course)

    print()

    # Printing student transcripts
    for student in root.students.values():
        student.print_transcript()
        print()

    # Close connection after all operations
    close_connection()
