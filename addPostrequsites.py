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

import os

from prerequsite_filters import findcourseID as findIDs

rootdir = 'C:/Users/duiba/Documents/UCSDCourses/'

# generator - generates the file names recursively
filenames = os.walk(rootdir)

# convert generator to list
filenames = list(filenames)

# save all the major abbreviations to majorabbs
majorabbs = filenames[0]

# get the contents only
for item in majorabbs:
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
                prerequsites = findIDs(pre)

                # now we get a list of prerequsites
                # we want to open them one by one and then write [course] into their fourth line
                # modulize this method so we can use it later to find prerequsites for the course

        except:
            print("no file named: " + course)
