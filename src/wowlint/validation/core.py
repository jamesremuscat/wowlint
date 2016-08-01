from enum import Enum


class Severity(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    FATAL = 3

    def __str__(self):
        return self.name

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


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
