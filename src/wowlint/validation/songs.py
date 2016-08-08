# -*- coding: utf-8 -*-
from enchant.checker import SpellChecker
import enchant

from wowlint.validation.core import Severity, Lint
from wowlint.wowfile import LicenseType, LineType


class BlockwiseLint(Lint):
    def validate_resource(self, song):
        issues = []
        for idx, block in enumerate(song.content.block):
            blockIssues = self.validate_block(idx, block)
            if blockIssues:
                issues += blockIssues
        return issues

    def validate_block(self, blockIndex, block):
        pass


class LinewiseLint(BlockwiseLint):
    def validate_block(self, blockIndex, block):
        issues = []
        for idx, line in enumerate(block.line):
            lineIssues = self.validate_line(blockIndex, idx, line)
            if lineIssues:
                issues += lineIssues
        return issues

    def validate_line(self, blockIndex, lineIndex, line):
        pass


class HasNoCopyright(Lint):
    message = "No copyright details provided"
    severity = Severity.ERROR

    def validate_resource(self, song):
        if song.content.copyright == "" and (not song.content.license or song.content.license.type == LicenseType.CCL):
            return [self.create_issue()]


class HasNoAuthor(Lint):
    message = "No author provided"
    severity = Severity.ERROR

    def validate_resource(self, song):
        if song.content.author == "":
            return [self.create_issue()]


class AllMinorWords(Lint):
    message = "Entirely uses minor words"
    severity = Severity.WARNING

    def validate_resource(self, song):
        for block in song.content.block:
            for line in block.line:
                if line.type == LineType.NORMAL:
                    return None
        return [self.create_issue()]


class TrailingComma(LinewiseLint):
    message = "({block}:{line}) Line has trailing comma"
    severity = Severity.WARNING

    def validate_line(self, blockIndex, lineIndex, line):
        if line.text.endswith(","):
            return [self.create_issue(blockIndex, lineIndex)]


class NoInitialCapital(LinewiseLint):
    message = "({block}:{line}) Line does not start with a capital letter"
    severity = Severity.WARNING

    def validate_line(self, blockIndex, lineIndex, line):
        if line.text[0] != line.text[0].upper():
            return [self.create_issue(blockIndex, lineIndex)]


def unSmartQuote(sillyString):
    return sillyString.\
        replace(u"’", "'").\
        replace(u"‘", "'").\
        replace(u"“", '"').\
        replace(u"”", '"')


class SpellCheck(LinewiseLint):
    message = u"({block}:{line}) Word is incorrectly spelt: '{word}'"
    severity = Severity.WARNING

    def __init__(self, config={}):
        LinewiseLint.__init__(self, config=config)
        self.checker = SpellChecker(enchant.DictWithPWL(config.get('lang', 'en_GB'), 'custom.dict'))

    def validate_line(self, blockIndex, lineIndex, line):
        issues = []
        self.checker.set_text(unSmartQuote(line.text))
        for err in self.checker:
            issues.append(self.create_issue(blockIndex, lineIndex, word=err.word))
        return issues


LINT_CLASSES = [
    HasNoCopyright,
    HasNoAuthor,
    TrailingComma,
    NoInitialCapital,
    AllMinorWords,
    SpellCheck
]
