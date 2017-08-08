from new_code.course import Course


class GraduateCourse(Course):
    """This represents a graduate-level course"""

    def __init__(self, course_id, name, content):
        super().__init__(course_id, name, content)
        self.course_level = self.__class__.__name__