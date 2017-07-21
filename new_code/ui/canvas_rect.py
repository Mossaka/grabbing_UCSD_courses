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