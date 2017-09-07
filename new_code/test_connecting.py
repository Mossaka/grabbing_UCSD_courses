import unittest
from pprint import pprint
from new_code.connecting import Connector

class TestConnector(unittest.TestCase):


    def testCoursePreNameList(self):
        courses = Connector().get_all_courses()
        for key, value in courses.items():
            pprint(value.get_pre_id_list())
