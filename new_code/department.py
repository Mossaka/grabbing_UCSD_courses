from new_code.major import Major


class Department(object):
    """ This represents a department object """
    def __init__(self):
        self.majors = {} # key as major code and value as major object
        self.main_url = None  # the main page url of the department
        self.name = None # the name of the deparment
        self.name_abbreviation = None # the name abbreviation of the deparment

        self.lower_courses = {}
        self.upper_courses = {}
        self.graduate_courses = {}
