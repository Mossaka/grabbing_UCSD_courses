from new_code.graduate_course import GraduateCourse
from new_code.lower_course import LowerCourse
from new_code.upper_course import UpperCourse


class Factory(object):
    """ a course factory that returns a course object by the type of the course"""

    def make_course(course_type, course_id, course_name, course_content):
        if course_type == "UpperCourse":
            return UpperCourse(course_id, course_name, course_content)
        elif course_type == "LowerCourse":
            return LowerCourse(course_id, course_name, course_content)
        elif course_type == "GraduateCourse":
            return GraduateCourse(course_id, course_name, course_content)
        assert 0, "bad course type: " + course_type
    make_course = staticmethod(make_course)