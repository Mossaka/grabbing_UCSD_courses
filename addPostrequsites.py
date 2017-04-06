'''

This module tries to add additional post-requsites courses to each course
in the fourth line. Since post-requsites courses are not explicitly showed in
website, this module is created specifically for finding the post-requsites
courses using pre-requsite courses and adding them to the course.

Code is not complete!

TODO:
    * use regex or other ways to parse the course ID from pre-requsite line 52
    * commenting and styling

'''

import os

rootdir = 'C:/Users/duiba/Documents/UCSDCourses/'
filenames = os.walk(rootdir)
#for name in filenames:
#    print(name)

filenames = list(filenames)

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
                print("course: "+ course + ". pre: "+ pre)
        except:
            print("no file named: " + course)
