import re

class Course:
    def __init__(self, course_id, name, content):
        self.course_id = self.string_correct(str(course_id))
        self.name = self.string_correct(str(name))
        self.content = str(content)
        self.prere = {}
        self.postre = {}
        self.description = ""
        self.prere_raw = ""
        self.seperate_content()

    def get_course_id(self):
        return self.course_id

    def set_course_id(self, course_id):
        self.course_id = course_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_content(self):
        return self.content

    def set_content(self, content):
        self.content = content

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_prere(self):
        return self.prere

    def get_postre(self):
        return self.postre

    def add_to_prere(self, pre_course):
        '''
        Add the prerequisite course to the prere dic
        '''
        self.prere[pre_course.get_course_id] = pre_course

    def add_to_postre(self, post_course):
        self.postre[post_course.get_course_id] = post_course

    def seperate_content(self):
        '''
        Seperate the content string to the description and prerequisite string
        content is in this form : "XXXX. Prerequisites: XXX"
        '''

        items = self.content.split("Prerequisites: ")
        if len(items) < 2:
            items.append("none.")

        self.description = self.string_correct(items[0].rstrip('\r\n'))
        self.prere_raw = items[1].rstrip('\r\n')

    def parse_course_pre_to_list(self):
        '''
        This method will transform prere_raw string to a list of course IDs
        '''
        prere_courses = []

        # convert non-word to spaces except "-"
        self.prere_raw = re.sub("[^\w]", " ", self.prere_raw)

        # split the string by spaces
        words = self.prere_raw.split()

        # iterate through words to find numbers
        for i in range(len(words)):

            previous_word = None
            if i is not 0:
                # define the previous word like MATH
                previous_word = words[i-1]

            # check if the string contains number, if True then the string is of the form: "140A"
            if words[i][0].isdigit():

                # course abbs = words[i-1]
                toappend = "{} {}".format(previous_word.upper(), words[i].upper())

                if toappend not in prere_courses:
                    prere_courses.append(toappend)

        return prere_courses

    def consecutive_break(self, constring):
        #TODO I need to finishi this function
        pass

    def string_correct(self, s):
        # correct string format
        s.replace('\n', '').replace('\t', '')
        s = " ".join(s.split())
        s = s.split('/')[0]
        return s