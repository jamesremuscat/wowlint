import os

from construct.core import ConstructError

from wowlint.validation.core import Severity, Issue
from wowlint.validation.songs import LINT_CLASSES as SONG_LINT_CLASSES
from wowlint.wowfile import Song


class Linter(object):
    def __init__(self, minSeverity=None, config={}):
        self.minSeverity = minSeverity

        self.songLints = map(lambda l: l(config.get(l.__name__, {})), SONG_LINT_CLASSES)

        self.known_files = {
            '.wow-song': (Song, self.songLints),
            '.wsg': (Song, self.songLints),
        }

    def lint(self, filename):
        issues = []
        ext = os.path.splitext(filename)[1]
        if ext in self.known_files:
            with open(filename, "rb") as f:
                try:
                    modelType, lints = self.known_files[ext]
                    model = modelType.parse(f.read())
                    for lint in lints:
                        if lint.severity >= self.minSeverity and self._shouldLintFile(lint, filename):
                            issues += lint.validate(model)
                except ConstructError as e:
                    Issue(Severity.FATAL, "{} Not a valid Words of Worship file".format(e.__class__.__name__)).add_to(issues)
        else:
            Issue(Severity.INFO, "Unrecognised file extension: {}".format(os.path.splitext(filename)[1])).add_to(issues)
        return issues

    def _shouldLintFile(self, lint, filename):
        if "exclude" in lint.config and filename in lint.config["exclude"]:
            return False
        return True
