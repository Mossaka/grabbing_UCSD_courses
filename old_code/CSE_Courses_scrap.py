'''
This file goes to "http://www.ucsd.edu/catalog/front/courses.html"
find all the links named "courses" and then grab the courses information
one by one.

For the given directory, this program will create a folder for every major
at UCSD. Then it creates a txt file for every course that major has inside
the folder. Each .txt file contains three lines:
    1. course complete name
    2. course description
    3. course prerequsites (unconverted*)

It takes about two minutes to run and covers >99% of all courses in UCSD
Some unstandarlized course description will not be written to the file,
but print the errors to the console.

Author: Jiaxiao Zhou
Update: 4/7/2017

'''
import os

import requests
from bs4 import BeautifulSoup as bs

from old_code.getAllLinks import getalllinks

rootdirctory = "C:/Users/duiba/Documents/UCSDCourses/"
testdirectory = "C:/Users/duiba/Documents/UCSDCoursesTest/"

def filterlist( list ):
    '''
    to eliminate empty contents in the list
    '''
    for item in list:
        if item.getText().strip() is None:
            list.remove(item)
        if item.getText().strip() is "":
            list.remove(item)
    return list

def getpartsfromlist(list, num):
    '''
    It seperates the course description and prerequisites
    :param list: a list of course descriptions
    :param num: the index for taking element from the list
    :return: a list of each course description or prerequisites
    '''
    toreturn = []
    for item in list:
        item = item.getText().split("Prerequisites: ")
        # in case when the prerequisites do not exist
        if(len(item) < 2):
            item.append("none.")
        item = item[num]
        item = item.rstrip('\r\n')
        toreturn.append(item)
    return toreturn

def populateidandnames(index, courseFields):
    '''
    populate the course IDs and names into a list
    :param index: 0 - IDs, 1 - Names
    :param courseFields: courseFiled such as MATH 140A
    :return: a list contains each all course IDs or all course names
    '''
    topopulate = []
    for courseField in courseFields:
        courseFieldText = courseField.getText()
        try:
            topopulate.append(courseFieldText.split('.')[index])
        except:
            # it does not have a ID?
            # TODO
            break
    return topopulate


def stringcorrent(s):
    '''
    correct the given string to a proper format
    '''
    s.replace('\n', '').replace('\t', '')
    s = " ".join( s.split() )
    s = s.split('/')[0]
    return s

def formatList(list):
    '''
    This function takes a list and then
    produce a new list with corrected strings
    '''
    temp = []
    for item in list:
        temp.append(stringcorrent(item))
    return temp

def writetofile(courseid, coursename, coursedes, prerequsites, path):
    with open(path+courseid+".txt", "w") as f:
        try:
            f.write(coursename + "\n")
            f.write(coursedes + "\n")
            f.write(prerequsites + "\n")
        except:
            print('failed to write')

def writefolderandcourses(link, rdirectory):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) "
                             "Chrome/22.0.1207.1 Safari/537.1"}
    courseabb = link.split('/')[-1].split('.')[0]
    main_url = link
    start_url = requests.get(main_url, headers=headers)
    bsObj = bs(start_url.text, 'lxml')

    # get the content tag
    content = bsObj.find("div", id="content")

    # get the course fields, including the course ids and actuall name
    courseFields = content.findAll("p", {"class": "course-name"})

    # get the descriptions courses
    courseDescriptions = filterlist(content.findAll("p", {"class": "course-descriptions"}))

    # get the prerequisites for the courses
    Prerequisites = getpartsfromlist(courseDescriptions, -1)
    courseDescriptions = formatList(getpartsfromlist(courseDescriptions, 0))
    courseId = formatList(populateidandnames(0, courseFields))
    courseNames = formatList(populateidandnames(1, courseFields))
    Prerequisites = formatList(Prerequisites)

    directory = rdirectory + courseabb + "/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    for index in range(len(courseId)):
        try:
            writetofile(courseId[index], courseNames[index],
                        courseDescriptions[index], Prerequisites[index],
                        directory)
        except:
            print("index out of range for major: " + courseabb + " and the course: " + courseId[index])
            print("length of courseid: " + str(len(courseId)))
            print("length of coursenames: " + str(len(courseNames)))
            print("length of coursedes: " + str(len(courseDescriptions)))
            print("length of prere: " + str(len(Prerequisites)))
            break


def main():

    links = getalllinks()
    # run each link one by one...
    '''
    TODO:
        any suggestions for efficiency improvements?
    '''
    for link in links:
        writefolderandcourses(link, rootdirctory)
    # one problem for BIOL webpage!!
    # okay, the problems are from the webpage..
    # nothing to do with it

if __name__ == '__main__' :
    main()