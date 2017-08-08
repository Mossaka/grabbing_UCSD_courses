import re

class Course(object):

    def __init__(self, course_id, name, content):
        """
        Initialize the course id, name, and content
        Notice that the course_id and name are pre_processed
        """
        # course id and name need to go over the string_correct function
        self.ID = self.id_correct(str(course_id))
        self.name = self.string_correct(str(name))

        self.content = str(content)

        # uninitialized variables
        self.prere = {}
        self.postre = {}
        self.description = None
        self.major_title = None
        self.course_level = None

        # parse description and prerequisite raw data from content var
        self.seperate_content()

    def get_course_id(self):
        """ get the course id"""
        return self.ID

    def set_course_id(self, course_id):
        """ set the course id"""
        self.ID = course_id

    def get_name(self):
        """ get the course name"""
        return self.name

    def set_name(self, name):
        """ set the course name"""
        self.name = name

    def get_content(self):
        """ get the course content"""
        return self.content

    def set_content(self, content):
        """ set the course content"""
        self.content = content

    def get_description(self):
        """ get the course description"""
        return self.description

    def set_description(self, description):
        """ set the course description"""
        self.description = description

    def get_major_title(self):
        """ get the major the course belongs """
        return self.major_title

    def set_major_title(self, title):
        self.major_title = title

    def get_prere(self):
        """ get the prerequsite courses. return a dic of Course object"""
        return self.prere

    def get_postre(self):
        """ get the postrequiste courses. return a dic of Course object"""
        return self.postre

    def add_to_prere(self, pre_course):
        """
        Add the prerequisite course to the prere dic
        """
        self.prere[pre_course.get_course_id] = pre_course

    def add_to_postre(self, post_course):
        """Add the postrequisite to the postre dic"""
        self.postre[post_course.get_course_id] = post_course

    def __str__(self):
        return self.ID

    def get_level(self):
        return self.course_level

    def get_pre_raw(self):
        return self.prere_raw

    def seperate_content(self):
        """
        Seperate the content string to the description and prerequisite string
        content is in this form : "XXXX. Prerequisites: XXX"
        """

        items = self.content.split("Prerequisites: ")
        if len(items) < 2:
            items.append("none.")

        self.description = self.string_correct(items[0].rstrip('\r\n'))
        self.prere_raw = items[1].rstrip('\r\n')

    # TODO those parsing methods should go to string process file (which will be created later) #
    def parse_course_pre_to_list(self):
        """
        This method will transform prere_raw string to a list of course IDs
        """
        prere_courses = []

        # convert non-word to spaces except "-"
        self.prere_raw = re.sub("[^\w-]", " ", self.prere_raw)

        # split the string by spaces
        words = self.prere_raw.split()

        # check if the string contains number, if True then the string is of the form: "140A"
        def append_to_list(word, previous_word):
            try:
                if word[0].isdigit():
                    toappend = None
                    # course abbs = words[i-1]
                    try:
                        toappend = "{} {}".format(previous_word.upper(), word.upper())
                    except AttributeError:
                        #TODO check this error for HIGR 216A-B
                        print("previous word is {}, word is {}".format(previous_word, word))
                    if toappend not in prere_courses:
                        prere_courses.append(toappend)
            except IndexError:
                #TODO why this would occur?
                print("word is {}, previous word is {}".format(word, previous_word))

        # iterate through words to find numbers
        for i in range(len(words)):

            previous_word = None
            if i is not 0:
                # define the previous word like MATH
                previous_word = words[i-1]

            if "-" in words[i]:
                num = re.split("[A-Z]", words[i])[0]
                letters = re.split("-", words[i])
                new_words = []
                for i in range(len(letters)):
                    if i is 0:
                        new_words.append(letters[0])
                    else:
                        new_words.append(num + letters[i])
                for word in new_words:
                    if word is not None and previous_word is not None:
                        append_to_list(word, previous_word)
                    else:
                        #TODO: what if the word is None?
                        pass
            else:
                append_to_list(words[i], previous_word)

        return prere_courses

    def string_correct(self, s):
        """ correct string format """
        s.replace('\n', '').replace('\t', '')
        s = " ".join(s.split())
        s = s.split('/')[0]
        return s

    def id_correct(self, s):
        """ correct id format """
        s.replace('\n', '').replace('\t', '')
        s = " ".join(s.split())
        return s

    __repr__ = __str__


