from enum import IntEnum


class Severity(IntEnum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    FATAL = 3

    def __str__(self):
        return self.name


class Lint(object):
    def create_issue(self, filename, block=0, line=0):
        return Issue(self.severity, filename, "{} {}".format(self.__class__.__name__, self.message.format(block=block, line=line)))


class Issue(object):
    def __init__(self, severity, sourceFile, message):
        self.severity = severity
        self.sourceFile = sourceFile
        self.message = message

    def __str__(self):
        return str([str(self.severity), self.sourceFile, self.message])

    def add_to(self, bucket):
        bucket.append(self)
