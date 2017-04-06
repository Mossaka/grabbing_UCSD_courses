import re
def findcourseID(prere):
    courseIDs = []
    words = re.sub("[^\w]", " ", prere).split()
    for i in range(len(words)):
        a = bool(re.search("\d", words[i]))
        if a is True:
            courseIDs.append(words[i-1].upper() + " " + words[i].upper())
    return courseIDs

findcourseID('BIMM 181 or BENG 181 or CSE 181, BIMM 182 or BENG 182 or CSE 182 or Chem 182.')