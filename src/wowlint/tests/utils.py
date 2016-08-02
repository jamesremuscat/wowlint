import os


def getTestFilePath(filename, curModule=__file__):
    return os.path.join(os.path.dirname(curModule), "data", filename)


def getTestFile(filename, curModule=__file__):
    return open(getTestFilePath(filename, curModule), "rb")
