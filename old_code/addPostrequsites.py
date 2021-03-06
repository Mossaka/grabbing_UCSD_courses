'''

This module tries to add additional post-requsites courses to each course
in the fourth line. Since post-requsites courses are not explicitly showed in
website, this module is created specifically for finding the post-requsites
courses using pre-requsite courses and adding them to the course.

Code is not complete!

TODO:
    * commenting and styling
    * add post requsite courses to the course
    * consider how to make applications out of the data

'''


#TODO: Make it more object-oriented

import os

from old_code.prerequsite_filters import consecutivebreak
from old_code.prerequsite_filters import containconsecutive
from old_code.prerequsite_filters import findcourseID
from old_code.prerequsite_filters import findcoursefile

rootdir = 'C:/Users/duiba/Documents/UCSDCourses/'

# generator - generates the file names recursively
filenames = os.walk(rootdir)

# convert generator to list
filenames = list(filenames)

# save all the major abbreviations to majorabbs
major_abbs = filenames[0]

def writetofile():
    # get the contents only
    majorabbs = major_abbs
    for item in major_abbs:
        if rootdir is not item and item is not []:
            majorabbs = item
            del filenames[0]
            break

    majorandcourse = {}
    allcours = []

    # get the rest courses for each major
    for index in range(len(majorabbs)):
        item = filenames[index][-1]
        if item is []:
            item = ["none"]
        majorandcourse[majorabbs[index]] = item

    for key, value in majorandcourse.items():
        for course in value:
            allcours.append(course)

    for major, courses in majorandcourse.items():
        for course in courses:
            try:
                with open(rootdir + major + "/" + course, 'r') as c:
                    lines = c.readlines()
                    pre = lines[-1]
                    with open("C:/Users/duiba/PycharmProjects/grabbing_UCSD_courses/prerequsites_data.txt", "a+") as f:
                        f.write(course + " :||: " + pre)
            except:
                print("no file named: " + course)

def addpostrequsites():
    '''
    temperately print all post-requisites courses
    '''
    a = "C:/Users/duiba/PycharmProjects/grabbing_UCSD_courses/"
    with open(a + "prerequsites_data.txt", "r") as f:
        lines = f.readlines()
        for line in lines:a
            courseids = line.split(":||:")[0] #the course id
            prerequsites = line.split(":||:")[-1] # the prerequisites of
            if containconsecutive(prerequsites):
                prerequsites = consecutivebreak(prerequsites)
            extractcourseids = findcourseID(prerequsites)
            for id in extractcourseids:
                if findcoursefile(id):
                    print(id + " postrequsites: " + courseids.split('.')[0])


def main():
    addpostrequsites()

if __name__ == '__main__':
    main()