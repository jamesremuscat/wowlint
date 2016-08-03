import os

from construct.core import ConstructError

from wowlint.validation.core import Severity, Issue
from wowlint.validation.songs import LINT_CLASSES as SONG_LINT_CLASSES
from wowlint.wowfile import Song


class Linter(object):
    def __init__(self, minSeverity=None, config={}):
        self.minSeverity = minSeverity
        self.config = config

        self.songLints = map(lambda l: l(config.get(l.__name__, {})), SONG_LINT_CLASSES)

    def lint(self, filename):
        issues = []
        with open(filename, "rb") as f:
            if filename.endswith(".wow-song") or filename.endswith(".wsg"):
                try:
                    song = Song.parse(f.read())
                    for lint in self.songLints:
                        if lint.severity >= self.minSeverity and self._shouldLintFile(lint, filename):
                            issues += lint.validate(song)
                except ConstructError as e:
                    Issue(Severity.FATAL, "{} Not a valid Words of Worship song file".format(e.__class__.__name__)).add_to(issues)
            else:
                Issue(Severity.INFO, "Unrecognised file extension: {}".format(os.path.splitext(filename)[1])).add_to(issues)
        return issues

    def _shouldLintFile(self, lint, filename):
        if lint.__class__.__name__ in self.config:
            lintConfig = self.config[lint.__class__.__name__]
            if "exclude" in lintConfig and filename in lintConfig["exclude"]:
                return False
        return True
