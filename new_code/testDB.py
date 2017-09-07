import unittest
from new_code.pymongoClient import MyMongoDB
from pprint import pprint

class TestDB(unittest.TestCase):

    def test_get_by_id(self):
        mydb = MyMongoDB()
        course = mydb.get_course("CSE 21")
        pprint(course)