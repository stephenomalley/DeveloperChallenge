import re


class Category(object):

    BASE_URL = "http://stackoverflow.com/questions"

    def __init__(self, url):
        self.url = url


class TypeCategory(Category):
    most_type = ["votes", "featured", "newest"]

    def __init__(self, types):
        Category.__init__(self, Category.BASE_URL+"?sort="+types)
        self.types = types


class TagCategory(Category):

    tags = ["Java", "PHP", "Python", "Python-2.7", "Python-3.x"]

    def __init__(self, tag):
        Category.__init__(self, Category.BASE_URL+"/tagged/"+tag)
        self.tag = tag
