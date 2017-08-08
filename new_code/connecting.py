import re

import requests
from bs4 import BeautifulSoup as bs

from new_code.course_factory import Factory

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                         "AppleWebKit/537.1 (KHTML, like Gecko) "
                         "Chrome/22.0.1207.1 Safari/537.1"}

# the main url for UCSD general course website
main_url = "http://ucsd.edu/catalog/front/courses.html"

# the front header for each major courses link
linkfront = "http://ucsd.edu/catalog/courses/"

# the max length for the course ID
MAX_ID_LENGTH = 40

# the choices of the user
CHOICE_1 = 1
CHOICE_2 = 2
CHOICE_3 = 3
CHOICE_4 = 4
CHOICE_5 = 5
CHOICE_6 = 6

class Connector:
    """
    Grab the courses information from the website, parse them to the Courses
    object and them parse both the prerequisites and postrequisites to them
    Inifinit loop for main application
    """
    def __init__(self):
        """
        Initialize the Beautiful Soup Object
        """
        start_url = requests.get(main_url, headers=headers)
        self.beautifulSoup_obj = bs(start_url.text, 'lxml') #beautiful soup object
        self.major_links = {}  # store links for all majors
        self.major_titles = {}  # store all major titles, using major abbreviation as keys
        self.courses = {}
        self._connected = False

    def parse_all_majors(self):
        """
        Go to the main general catalog website and find all major links
        Store the links to major_links
        """

        # find the content div tag
        content = self.beautifulSoup_obj.find("div", id="content")

        # find links by looking for <a>
        links = content.findAll("a")
        # check if "courses" is in the link
        for link in links:
            if 'courses' in link:
                major_abbreviation = link['href'].split("/")[-1] # get the abbreviation for the major
                self.major_links[major_abbreviation.split('.')[0]] = linkfront + major_abbreviation
                self.major_titles[linkfront + major_abbreviation] = link.get('title')

    def parse_courses(self, url):
        """
        parse the courses from url to create Courses dic
        :param url: the given url for the major that contains all its courses
        """
        # get the content tag
        try:
            start_url = requests.get(url, headers=headers)
        except ConnectionError:
            return False
        except requests.exceptions.ConnectionError:
            print("parse course fails for url: {}".format(url))
            return False
        self.beautifulSoup_obj = bs(start_url.text, 'lxml')
        page_content = self.beautifulSoup_obj.find('div', id='content')

        # get the course fields, including the course ids and actuall name
        courseFields = page_content.findAll("p", {"class": "course-name"})

        # Seperate course IDs and course names
        courseIDs = []
        courseNames = []

        # courseField contains both the name and id.
        for field in courseFields:

            # seperate the name and id by "."
            id_names = field.getText().split('.')
            if len(id_names) >= 2: # the normal string
                courseIDs.append(id_names[0])
                courseNames.append(id_names[1])

            # when the id contains the name, seperate them by ":'
            elif len(id_names[0]) > MAX_ID_LENGTH:
                courseIDs.append(id_names[0].split(":")[0])
                courseNames.append(id_names[0].split(":")[-1])
            # if neither ways could seperate them, then store the exact copy
            # of them
            #TODO: need to think about a better way to solve this issue
            else:
                courseIDs.append(id_names[0])
                courseNames.append(id_names[0])
        # get the descriptions courses
        course_des = self.filterlist(page_content.findAll("p",
                                            {"class": "course-descriptions"}))
        # if the data is in standard form, the length of names, ids and
        # descriptions should be the same
        if len(course_des) == len(courseIDs) == len(courseNames):

            # make course object and store it to the courses dic
            self.make_Courses(url, course_des, courseIDs, courseNames)

        # if not, use the second way, find the course field and assume the next
        # paragraph tag be the description
        else:
            # clear the courses_des
            del course_des[:]
            # for each field, find the next paragraph and store it to the
            # course_des
            for field in courseFields:
                course_des.append(field.findNext("p"))
            # check length
            if len(course_des) == len(courseIDs) == len(courseNames):
                self.make_Courses(url, course_des, courseIDs, courseNames)
            else:
                # if both ways do not work, print out the url and the lengths
                print("the url: {} has problem".format(url))
                print("the length of des is: {}".format(len(course_des)))
                print("the length of ids is: {}".format(len(courseIDs)))
                print("the length of names is: {}".format(len(courseNames)))
        return True

    def filterlist(self, content_list):
        '''
        to eliminate empty contents in the list
        :param content_list the given list
        '''
        for item in content_list:
            if item.getText().strip() is None:
                content_list.remove(item)
            if item.getText().strip() is "":
                content_list.remove(item)
        return content_list

    def _InspectCourseLevel(self, course_ID):
        """ a private method for parsing the course level """
        #TODO there should be a structure change: all the string parsing should go to another class
        #TODO connecting file should only deal with connecting issues
        try:
            _second_half = course_ID.split()[-1]
            _number_only = re.split("[A-Z]", _second_half)[0]
        except IndexError:
            print(course_ID)
            return None
        try:
            _level = int(_number_only)
            if _level >= 200:
                return "GraduateCourse"
            elif _level >= 100:
                return "UpperCourse"
            else:
                return "LowerCourse"
        except ValueError:
            print(course_ID)
            return None

    def make_Courses(self, url, course_des, courseIDs, courseNames):
        """
        create a Course object and uses its id as a key to store to the
        courses dictionary
        :param url, for the key to the hashtable of courselevel
        :param course_des: the description of the course
        :param courseIDs:  the id of the course
        :param courseNames: the name of the course
        :return:
        """
        for i in range(len(course_des)):
            if self._InspectCourseLevel(courseIDs[i]):
                self.courses[courseIDs[i]] = Factory.make_course( self._InspectCourseLevel(courseIDs[i]),
                                            courseIDs[i], courseNames[i], course_des[i].getText())
                #TODO integrate this to the factory
                self.courses[courseIDs[i]].set_major_title(self.major_titles[url])

    def parse_prerequisites(self):
        """ parse the prerequisite courses into each course """
        for key in self.courses:
            pre_list = self.courses[key].parse_course_pre_to_list()
            for id_string in pre_list:
                if id_string in self.courses.keys():
                    self.courses[key].add_to_prere(self.courses[id_string])

    def parse_postrequsites(self):
        """ parse the post-requisite ourses into each course """
        for key in self.courses:
            pre_courses = self.courses[key].get_prere()
            for key_p in pre_courses:
                pre_courses[key_p].add_to_postre(self.courses[key])
        self._connected = True

    @property
    def connected(self):
        return self._connected

    def find_course(self, course_id):
        try:
            _ = self.courses[course_id]
            return True
        except KeyError:
            return False

    def get_course(self, course_id):
        return self.courses[course_id]

    # No longer needed. A GUI is developed for replacing the command-line program
    def run(self):
        #runs the main program
        self.parse_all_majors()
        print("---start parsing courses from websites---")
        for ab, link in self.major_links.items():
            self.parse_courses(link)

        print("Parsing success!")
        print("---start parsing prerequisites and postrequisites---")

        self.parse_prerequisites()
        self.parse_postrequsites()
        print("Parsing success!")


        while True:
            print("-------------Please enter a course ID or enter 0 to Exit-----------------")
            course_id = input()
            if course_id is 0:
                break
            course_id = course_id.upper()
            while course_id in self.courses.keys():
                print("please select the item you want")
                print("1. course name")
                print("2. course description")
                print("3. course pre-requisites")
                print("4. course post-requisites")
                print("5. course pre-requisite raw data (no slice)")
                print("6. Exit")
                number = input()
                try:
                    number = int(number)
                    if number == CHOICE_1:
                        print("the course name for " + course_id + " is " +
                              self.courses[course_id].get_name())
                    elif number == CHOICE_2:
                        print("the course description for " + course_id + " is " +
                              self.courses[course_id].get_description()
                        )
                    elif number == CHOICE_3:
                        print("the course pre-requisites for {} are:".format(str(course_id)))
                        precourses = self.courses[course_id].get_prere()
                        for key in precourses:
                            print(precourses[key].get_course_id(), " ")
                    elif number == CHOICE_4:
                        print("the course post-requisites for {} are:".format(str(course_id)))
                        postcourses = self.courses[course_id].get_postre()
                        for key in postcourses:
                            print(postcourses[key].get_course_id(), " ")
                    elif number == CHOICE_5:
                        print("the course pre-requisite raw data is " + self.courses[course_id].get_pre_raw())
                    elif number == CHOICE_6:
                        break
                except ValueError:
                    print("we don't have this selection choice")
                    continue
            else:
                print("we don't find this course, please enter another one")

if __name__ == "__main__":
    #Main().parse_courses("http://ucsd.edu/catalog/courses/SOC.html")
    Connector().run()
