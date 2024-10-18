import persistent


class Course(persistent.Persistent):
    def __init__(self, id, name="", credit=0, gradeScheme=None):
        self.id = id
        self.name = name
        self.credit = credit
        self.gradeScheme = gradeScheme if gradeScheme is not None else []

    def __str__(self):
        return "ID: %d Course: %s, Credit: %d" % (self.id, self.name, self.credit)

    def getCredit(self):
        return self.credit

    def setName(self, name: str):
        self.name = name

    def scoreGrading(self, score):
        self.gradeScheme.sort(key=lambda x: x["min_score"])
        for grade_range in self.gradeScheme:
            if grade_range["min_score"] <= score <= grade_range["max_score"]:
                return grade_range["grade"]
        return "F"

    def setGradeScheme(self, scheme):
        if all(
            isinstance(item, dict)
            and "min_score" in item
            and "max_score" in item
            and "grade" in item
            for item in scheme
        ):
            # Ensure the scheme has valid structure
            self.gradeScheme = scheme
        else:
            raise ValueError(
                "Invalid grade scheme format. Each entry must have 'min_score', 'max_score', and 'grade'."
            )

    def print_detail(self):
        print(self.__str__())


class Student(persistent.Persistent):
    def __init__(self, id, name="", password: str = ""):
        self.id = id
        self.name = name
        self.enrolls = []
        self.password = password

    def enroll_course(self, course, score=0):
        enrollment = Enrollment(course=course, student=self, score=score)
        self.enrolls.append(enrollment)
        return enrollment

    def getEnrollment(self, course):
        for enrollment in self.enrolls:
            if enrollment.course == course:
                return enrollment
        return None

    def print_transcript(self):
        total_credits = 0
        total_points = 0.0
        print(f"Transcript for {self.name}")
        print(f"{'Course':<20}{'Credits':<10}{'Score':<10}{'Grade'}")
        print("-" * 50)

        for enrollment in self.enrolls:
            course = enrollment.course
            grade = (
                enrollment.getGrade()
            )  # Get grade based on score and course grading scheme
            score = enrollment.getScore()
            print(f"{course.name:<20}{course.credit:<10}{score:<10}{grade}")
            total_credits += course.credit
            grade_points = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}.get(
                grade, 0.0
            )
            total_points += grade_points * course.credit

        gpa = total_points / total_credits if total_credits > 0 else 0.0
        print("-" * 40)
        print(f"Total Credits: {total_credits}")
        print(f"GPA: {gpa:.2f}")

    def setName(self, name: str):
        self.name = name

    def login(self, password: str):
        if password == self.password:
            return True
        else:
            return False
class Enrollment(persistent.Persistent):
    def __init__(self, course, student, score=0):
        self.course = course
        self.student = student
        self.score = score

    def getCourse(self):
        return self.course

    def getGrade(self):
        # Get the grade based on the course's grading scheme and the student's score
        return self.course.scoreGrading(self.score)

    def printDetail(self):
        print(
            f"Enrollment: {self.student.name} in {self.course.name} with score {self.score} and grade {self.getGrade()}"
        )

    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score
