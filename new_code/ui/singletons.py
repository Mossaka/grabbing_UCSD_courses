from new_code.ui.singleton import Singleton

@Singleton
class AllCourses:
    def __init__(self):
        self._allcourses = {}

    @property
    def allcourses(self):
        return self._allcourses

    @allcourses.setter
    def allcourses(self, courses):
        self._allcourses = courses


@Singleton
class Canvas:
    def __init__(self):
        self._canvas = None

    @property
    def canvas(self):
        return self._canvas

    @canvas.setter
    def canvas(self, canvas):
        self._canvas = canvas

@Singleton
class CoursePlannerSingleton:
    def __init__(self):
        self._course_planner = None

    @property
    def course_planner(self):
        return self._course_planner

    @course_planner.setter
    def course_planner(self, course_planner):
        self._course_planner = course_planner