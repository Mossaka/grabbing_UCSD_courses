import requests
from bs4 import BeautifulSoup as bs

from course import Course

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                         "AppleWebKit/537.1 (KHTML, like Gecko) "
                         "Chrome/22.0.1207.1 Safari/537.1"}
main_url = "http://ucsd.edu/catalog/front/courses.html"
linkfront = "http://ucsd.edu/catalog/courses/"

class Main:

    def __init__(self):
        start_url = requests.get(main_url, headers=headers)
        self.bsObj = bs(start_url.text, 'lxml')
        self.major_links = {}
        self.courses = {}

    def parse_all_majors(self):
        content = self.bsObj.find("div", id="content")
        links = content.findAll("a", href=True)
        for link in links:
            if 'courses' in link:
                major_ab = link['href'].split("/")[-1]
                self.major_links[major_ab.split('.')[0]] = linkfront + major_ab



    def parse_courses(self, url):

        # get the content tag
        start_url = requests.get(url, headers=headers)
        self.bsObj = bs(start_url.text, 'lxml')
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

        if len(courseDescriptions) == len(courseIDs) == len(courseNames):

            for i in range(len(courseDescriptions)):
                self.courses[courseIDs[i]] = Course(courseIDs[i], courseNames[i],
                                                    courseDescriptions[i].getText())

            for key in self.courses:
                print( str( self.courses[key] ) )

        else:
            print("the course info has problems for the url: {}".format(url))
            print("the length of descriptions is: {}".format(len(courseDescriptions)))
            print("the length of ids is: {}".format(len(courseIDs)))
            print("the length of names is: {}".format(len(courseNames)))



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

    def run(self):
        """runs the main program"""
        self.parse_all_majors()
        for ab, link in self.major_links.items():
            self.parse_courses( link )

if __name__ == "__main__":
    Main().parse_courses("http://ucsd.edu/catalog/courses/RSM.html")
