# grabbing_UCSD_courses

This project will automatically grab over 5500 courses at UCSD and download into your computer.
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
