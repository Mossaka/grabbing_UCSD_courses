import requests
from bs4 import BeautifulSoup as bs

from course import Course

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                         "AppleWebKit/537.1 (KHTML, like Gecko) "
                         "Chrome/22.0.1207.1 Safari/537.1"}
main_url = "http://ucsd.edu/catalog/courses/CSE.html"
start_url = requests.get(main_url, headers=headers)

class Main:

    def __init__(self):
        self.bsObj = bs(start_url.text, 'lxml')
        self.courses = {}

    def parse_courses(self):

        # get the content tag
        page_content = self.bsObj.find('div', id='content')

        # get the course fields, including the course ids and actuall name
        courseFields = page_content.findAll("p", {"class": "course-name"})

        # Seperate course IDs and course names
        courseIDs = []
        courseNames = []
        for field in courseFields:
            id_names = field.getText().split('.')
            if len(id_names) >= 2:
                courseIDs.append(id_names[0])
                courseNames.append(id_names[-1])
            else:
                print("{} does not have name or id".format(field.getText()))

        # get the descriptions courses
        courseDescriptions = self.filterlist(page_content.findAll("p",
                                            {"class": "course-descriptions"}))

        assert len(courseDescriptions) == len(courseIDs) == len(courseNames)

        for i in range(len(courseDescriptions)):
            self.courses[courseIDs[i]] = Course(courseIDs[i], courseNames[i], courseDescriptions[i].getText())

        print("CSE 100 prerequisites are: {}".format(self.courses["CSE 100"].parse_course_pre_to_list()))


    def filterlist(self, content_list):
        '''
        to eliminate empty contents in the list
        '''
        for item in content_list:
            if item.getText().strip() is None:
                content_list.remove(item)
            if item.getText().strip() is "":
                content_list.remove(item)
        return content_list

if __name__ == "__main__":
    Main().parse_courses()