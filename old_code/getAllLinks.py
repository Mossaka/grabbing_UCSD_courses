'''
This module returns all the links to the course of different majors at UCSD as a list
'''

def getalllinks():
    import requests
    from bs4 import BeautifulSoup as bs

    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) "
                                 "Chrome/22.0.1207.1 Safari/537.1"}
    main_url = "http://ucsd.edu/catalog/front/courses.html"
    start_url = requests.get(main_url, headers=headers)

    bsObj = bs(start_url.text, 'lxml')

    # get the content tag
    content = bsObj.find("div",id="content")

    links = content.findAll("a", href=True)
    courseLinks = []
    for link in links:
        if 'courses' in link:
            courseLinks.append(link['href'].split('/')[-1])

    linkfront = "http://ucsd.edu/catalog/courses/"

    courseLinksC = []
    for link in courseLinks:
        a = linkfront+link
        courseLinksC.append(a)
    return(courseLinksC)