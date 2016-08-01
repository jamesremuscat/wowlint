import os

from construct.core import FieldError
from enum import Enum
from wowlint.wowfile import Song


class Severity(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    FATAL = 3

    def __str__(self):
        return self.name


class Issue(object):
    def __init__(self, severity, sourceFile, message):
        self.severity = severity
        self.sourceFile = sourceFile
        self.message = message

    def __str__(self):
        return str([str(self.severity), self.sourceFile, self.message])

    def add_to(self, bucket):
        bucket.append(self)


class Linter(object):
    def lint(self, filename):
        issues = []
        with open(filename, "rb") as f:
            if filename.endswith(".wow-song") or filename.endswith(".wsg"):
                try:
                    song = Song.parse(f.read())
                except FieldError:
                    Issue(Severity.FATAL, filename, "Not a valid Words of Worship song file").add_to(issues)
            else:
                Issue(Severity.INFO, filename, "Unrecognised file extension: {}".format(os.path.splitext(filename)[1])).add_to(issues)
        return issues
