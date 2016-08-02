import os


def getTestFile(filename):
    path = os.path.join(os.path.dirname(__file__), "data", filename)
    return open(path, "rb")
