from new_code.course import Course


class UpperCourse(Course):

    """This represents a upper division course"""
    def __init__(self, course_id, name, content):
        super().__init__(course_id, name, content)
        self.course_level = self.__class__.__name__