from new_code.ui_activities.course_planner.course_paint import CoursePaint


class CoursePaintFactory:
    def __init__(self, x, y, width=10, height=10, color=None, id=None, canvas=None):
        self.course_paint = CoursePaint(x,y,width=width,height=height,color=color,id=id,canvas=canvas)

    def paint_course(self, div=None, major=None, quarter=None):
        return self.course_paint

    def get_painted_courses(self):
        pass

