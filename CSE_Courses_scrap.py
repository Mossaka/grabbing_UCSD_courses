import requests
from bs4 import BeautifulSoup as bs
from urllib.error import HTTPError
import os
import re
import csv
from getAllLinks import getalllinks

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
    toreturn = []
    for item in list:
        item = item.getText().split("Prerequisites: ")
        if(len(item) < 2):
            item.append("none.")
        item = item[num]
        item = item.rstrip('\r\n')
        toreturn.append(item)
    return toreturn

def populateidandnames(topopulate, index, courseFields):
    for courseField in courseFields:
        courseFieldText = courseField.getText()
        try:
            topopulate.append(courseFieldText.split('.')[index])
        except:
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

def main():
    # setup
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) "
                             "Chrome/22.0.1207.1 Safari/537.1"}

    links = getalllinks()
    for link in links:

        courseabb = link.split('/')[-1].split('.')[0]
        main_url = link
        start_url = requests.get(main_url, headers=headers)
        bsObj = bs(start_url.text, 'lxml')

        # get the content tag
        content = bsObj.find("div",id="content")

        # get the course fields, including the course ids and actuall name
        courseFields = content.findAll("p", {"class":"course-name"})

        # get the descriptions courses
        courseDescriptions = filterlist(content.findAll("p", {"class":"course-descriptions"}))

        # get the prerequisites for the courses
        Prerequisites = getpartsfromlist(courseDescriptions, -1)
        courseDescriptions = formatList( getpartsfromlist(courseDescriptions, 0) )
        courseId = formatList(populateidandnames([], 0, courseFields))
        courseNames = formatList(populateidandnames([], 1, courseFields))
        Prerequisites = formatList(Prerequisites)

        directory = "C:/Users/duiba/Documents/UCSDCourses/" + courseabb + "/"

        if not os.path.exists(directory):
            os.makedirs(directory)


        for index in range(len(courseId)):
            try:
                writetofile(courseId[index], courseNames[index],
                        courseDescriptions[index], Prerequisites[index],
                        directory)
            except:
                print("index out of range for major: " + courseabb + " and the course: " + courseId[index] )
                print("length of courseid: " + str(len(courseId)))
                print("length of coursenames: " + str(len(courseNames)))
                print("length of coursedes: " + str(len(courseDescriptions)))
                print("length of prere: " + str(len(Prerequisites)))
                break




    '''with open("CSECourses.txt", "a+") as f:
        f.write("id, name, description\n")
        for courseName in courseNames:
            try:
                temp = courseName.split('\n')
                f.write(courseId[i] +", " + temp[0].rstrip('\r\n') + \
                        temp[1].strip() + ", " + Prerequisites[i].split(",")[0].rstrip('\n') +"\n")
                i += 1
            except:
                f.write(courseId[i] + ", " + courseName + ", " + \
                        Prerequisites[i].split(",")[0].rstrip('\n') + "\n")
                i += 1'''


main()