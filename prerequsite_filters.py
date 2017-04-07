import os
import re

'''
TODO:
    convert Math 20A, or 20B, and 20F to
            MATH 20A MATH 20B MATH 20F
'''

def containconsecutive(prere):
    '''
    check if the given string contains consecutive courses, such as Math 20A-B-C-D
    :param prere: the prerequsites string
    :return: True if it contains consecutive courses
    '''
    if "A-B" in prere or "A-B-C" in prere or "A-B-C-D" in prere or "A-B-C-D-E" in prere:
        return prere
    else:
        return None

def consecutivebreak(constring):
    '''
    this function breaks the consecutive courses and convert them to individual courses
    for example:
        input: MATH 140A-B-C
        outpu: MATH 140A MATH 140B MATH 140C
    :param constring: the given string that contains consecutive coureses
    :return: the correct form of prerequsites
    '''

    # filter the string to get rid of any non-word except "-"
    words = re.sub("[^\w-]", " ", constring).split()

    for i in range(len(words)):

        # find the consecutive word
        if "A-B" in words[i]:

            # the course abbreviation, such as MATH
            courseAbb = words[i-1]

            # the number, such as 140 from 140A-B-C
            number = words[i].split("A")[0]

            coursenums = words[i].split("-")

            # bond the course abbs and number to the letters to form complete course id
            for j in range(len(coursenums)):
                if j == 0:
                    words[i] = coursenums[j] + " "
                else:
                    words[i] += ( courseAbb + " " + number + coursenums[j] + " ")

    toreturn = ""
    for word in words:
        toreturn += word + " "
    return  toreturn

def findcourseID(prere):
    '''
    extract course ids from a given string (the string must not have consecutive courses!)
    :param prere: the prerequsite string
    :return: a list of course ids, such as ["MATH 140A", "MATH 140B", "MATH 140C"]
    '''
    courseIDs = []
    words = re.sub("[^\w]", " ", prere).split()
    for i in range(len(words)):
        # check if the string contains number, if True then the string is of the form: "140A"
        a = bool(re.search("\d", words[i]))
        if a is True:
            # course abbs = words[i-1]
            toappend = words[i-1].upper() + " " + words[i].upper()
            if toappend not in courseIDs:
                courseIDs.append(toappend)
    return courseIDs

#def writepostretofile(course, filestowrite)

def findcoursefile(courseid):
    '''
    check UCSDcourses folder to see if the given courseid is a actual file in my computer
    :param courseid: the course id such as MATH 140A
    :return: True if my computer contains such course file
    '''
    rootdir = 'C:/Users/duiba/Documents/UCSDCourses/'
    toappend = ".txt"
    course_abb = courseid.split(" ")[0]
    majordir = rootdir + course_abb + "/"
    coursedir = majordir + courseid + toappend
    return os.path.exists(coursedir)

def main():
    courseids = findcourseID("PHYS 100A 105A and MATH 20A MATH 20B MATH 20C MATH 20D MATH 20E  and 20F or 18 Open to major codes EC28 PY26 ")
    for courseid in courseids:
        print(courseid)
        print(findcoursefile(courseid))
    #for course in courselist:
    #    print(course)
if __name__ == '__main__' :
    main()