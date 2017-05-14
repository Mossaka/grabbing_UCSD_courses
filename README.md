# grabbing_UCSD_courses

This project will automatically grab over 5500 courses at UCSD and download into your computer.
This file goes to "http://www.ucsd.edu/catalog/front/courses.html"
find all the links named "courses" and then grab the courses information
one by one.

Old_code:
    For the given directory, this program will create a folder for every major
    at UCSD. Then it creates a txt file for every course that major has inside
    the folder. Each .txt file contains three lines:
        1. course complete name
        2. course description
        3. course prerequsites (unconverted*)

    It takes about two minutes to run and covers >99% of all courses in UCSD
    Some unstandarlized course description will not be written to the file,
    but print the errors to the console.
New_code:
    This uses the ideas of Object Oriented Programming. Instead of writting functions to do
    seperate things, I created a class named course and associates the name, id and content 
    to it. It makes life much easier! Now the program will parse the prerequisites and
    postrequisite couses into the course object and it has a little command-line interaction
    between the machine and the user. 
    
    When the program starts running, it will ask you to enter the course id. For example,
    you can enter "cse 100", then it will give you 6 oprations. 
    1. see the course name
    2. see the course description
    3. see the course prerequisite courses
    4. see the course postrequisite courses
    5. see the course prerequisite raw data (string)
    6. exit
    
    The interaction is a lot of fun ane really saves time for course shopping!
