from wowlint.validation.core import Severity, Lint
from wowlint.wowfile import LicenseType


class BlockwiseLint(Lint):
    def validate(self, filename, song):
        issues = []
        for idx, block in enumerate(song.block):
            blockIssues = self.validate_block(filename, idx, block)
            if blockIssues:
                issues += blockIssues
        return issues

    def validate_block(self, filename, blockIndex, block):
        pass


class LinewiseLint(BlockwiseLint):
    def validate_block(self, filename, blockIndex, block):
        issues = []
        for idx, line in enumerate(block.line):
            lineIssues = self.validate_line(filename, blockIndex, idx, line)
            if lineIssues:
                issues += lineIssues
        return issues

    def validate_line(self, filename, blockIndex, lineIndex, line):
        pass


class HasNoCopyright(Lint):
    def __init__(self):
        self.message = "No copyright details provided"
        self.severity = Severity.ERROR

    def validate(self, filename, song):
        if song.copyright == "" and (not song.license or song.license.type == LicenseType.CCL):
            return [self.create_issue(filename)]


class HasNoAuthor(Lint):
    def __init__(self):
        self.message = "No author provided"
        self.severity = Severity.ERROR

    def validate(self, filename, song):
        if song.author == "":
            return [self.create_issue(filename)]


class TrailingComma(LinewiseLint):
    def __init__(self):
        self.message = "({block}:{line}) Line has trailing comma"
        self.severity = Severity.WARNING

    def validate_line(self, filename, blockIndex, lineIndex, line):
        if line.text.endswith(","):
            return [self.create_issue(filename, blockIndex, lineIndex)]


LINTS = [
    HasNoCopyright(),
    HasNoAuthor(),
    TrailingComma()
]
