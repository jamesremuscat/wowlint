import os


def getTestFile(filename, curModule=__file__):
    path = os.path.join(os.path.dirname(curModule), "data", filename)
    return open(path, "rb")
