import pymongo
from pprint import pprint
from new_code.connecting import Connector

class MongoDriver:
    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

    def get_client(self):
        client_str = "mongodb://{}:{}@cluster0-shard-00-00-cu7pm.mongodb.net:27017,cluster0-shard-00-01-cu7pm.mongodb.net:27017,cluster0-shard-00-02-cu7pm.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
        complete_client_str = client_str.format(self.user_name, self.password)
        return pymongo.MongoClient(complete_client_str)


class MyMongoDB:

    def __init__(self):
        self.db = self.get_db()
        self.ucsd_course_collection = self.db.ucsd_courses

    def get_db(self):
        return MongoDriver("Mossaka", "uzu3210008").get_client()['mydb']

    def update_db(self):  # TODO: make this a multi-threaded
        courses_dict = Connector().get_all_courses()
        for course_id, course_obj in courses_dict.items():
            course_doc = {
                "ID": course_obj.get_course_id(),
                "Name:": course_obj.get_name(),
                "Description": course_obj.get_description(),
                "Level": course_obj.get_level(),
                "Prerequisites": course_obj.get_pre_id_list(),
                "Postrequisites": course_obj.get_post_id_list(),
                "DepartmentName": course_obj.get_major_title(),
            }
            self.ucsd_course_collection.insert_one(course_doc)

    def get_course(self, course_id):
        return self.ucsd_course_collection.find_one({"ID": course_id})




client = pymongo.MongoClient("mongodb://Mossaka:uzu3210008@cluster0-shard-00-00-cu7pm.mongodb.net:27017,cluster0-shard-00-01-cu7pm.mongodb.net:27017,cluster0-shard-00-02-cu7pm.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = client.mydb
ucsd_courses = db.ucsd_courses
post = {
    "CourseID": "CSE 11",
    "Major": "Computer Engineering",
    "Department": "Computer Science and Engineering",
    "Unit": 4,
}
post_id = ucsd_courses.insert_one(post).inserted_id

pprint(ucsd_courses.find_one({"_id": post_id}))