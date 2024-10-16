import persistent
import BTrees

class Course(persistent.Persistent):
    def __init__(self, course_id: int, course_name: str, credit: int, grading_scheme: list[dict]):
        self.course_id = course_id
        self.course_name = course_name
        self.credit = credit
        self.grading_scheme = grading_scheme