# -*- coding: utf-8 -*-
from enchant.checker import SpellChecker
import enchant

from wowlint.validation.core import Lint, Severity


def unSmartQuote(sillyString):
    return sillyString.\
        replace(u"’", "'").\
        replace(u"‘", "'").\
        replace(u"“", '"').\
        replace(u"”", '"')


class LiturgyLinewiseLint(Lint):
    def validate_resource(self, liturgy):
        issues = []
        for idx, line in enumerate(liturgy.content.line):
            lineIssues = self.validate_line(idx, line)
            if lineIssues:
                issues += lineIssues
        return issues

    def validate_line(self, idx, line):
        pass


class SpellCheck(LiturgyLinewiseLint):
    message = u"(line {line}) Word is incorrectly spelt: '{word}'"
    severity = Severity.WARNING

    def __init__(self, config={}):
        LiturgyLinewiseLint.__init__(self, config=config)
        self.checker = SpellChecker(enchant.DictWithPWL(config.get('lang', 'en_GB'), 'custom.dict'))

    def validate_line(self, lineIndex, line):
        issues = []
        self.checker.set_text(unSmartQuote(line.text))
        for err in self.checker:
            issues.append(self.create_issue(line=lineIndex, word=err.word))
        return issues

LINT_CLASSES = [
    SpellCheck
]
