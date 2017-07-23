class CoursePaint:
    def __init__(self, x, y, width=10, height=10, color=None, outline=None, id=None):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color = color
        self._outline = outline
        self._id = id
        self._ui_id = None

    @property
    def ui_id(self):
        return self._ui_id

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def color(self):
        return self._color

    @property
    def outline(self):
        return self._outline

    @property
    def id(self):
        return self._id

    @width.setter
    def width(self, width):
        self._width = width

    @height.setter
    def height(self, height):
        self._height = height

    @color.setter
    def color(self, color):
        self._color = color

    @outline.setter
    def outline(self, outline):
        self._outline = outline

    @id.setter
    def id(self, id):
        self._id = id\

    @x.setter
    def x(self, x):
        self._x = x

    @y.setter
    def y(self, y):
        self._y = y

    @ui_id.setter
    def ui_id(self, ui_id):
        self._ui_id = ui_id
