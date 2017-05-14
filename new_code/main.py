import requests
from bs4 import BeautifulSoup as bs

from new_code.course import Course

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

class Main:
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
        self.course_count = 0
        self.bsObj = bs(start_url.text, 'lxml')
        self.major_links = {}
        self.courses = {}

    def parse_all_majors(self):
        """
        Go to the main general catalog website and find all major links
        Store the links to major_links
        """

        # find the content div tag
        content = self.bsObj.find("div", id="content")
        # find links by looking for a
        links = content.findAll("a", href=True)
        for link in links:
            # check if "courses" is in the link
            if 'courses' in link:
                major_ab = link['href'].split("/")[-1]
                self.major_links[major_ab.split('.')[0]] = linkfront + major_ab



    def parse_courses(self, url):
        """
        parse the courses from url to create Courses dic
        :param url: the given url for the major that contains all its courses
        """
        # get the content tag
        start_url = requests.get(url, headers=headers)
        self.bsObj = bs(start_url.text, 'lxml')
        page_content = self.bsObj.find('div', id='content')

        # get the course fields, including the course ids and actuall name
        courseFields = page_content.findAll("p", {"class": "course-name"})
        self.course_count += len(courseFields)

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
            self.make_Courses(course_des, courseIDs, courseNames)

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
                self.make_Courses(course_des, courseIDs, courseNames)
            else:
                # if both ways do not work, print out the url and the lengths
                print("the url: {} has problem".format(url))
                print("the length of des is: {}".format(len(course_des)))
                print("the length of ids is: {}".format(len(courseIDs)))
                print("the length of names is: {}".format(len(courseNames)))



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

    def make_Courses(self, course_des, courseIDs, courseNames):
        """
        create a Course object and uses its id as a key to store to the
        courses dictionary
        :param course_des: the description of the course
        :param courseIDs:  the id of the course
        :param courseNames: the name of the course
        :return:
        """
        for i in range(len(course_des)):
            self.courses[courseIDs[i]] = Course(courseIDs[i], courseNames[i],
                                                course_des[i].getText())

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

    def run(self):
        """runs the main program"""
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
    Main().run()
