from unittest.case import TestCase

from wowlint.linter import Linter
from wowlint.tests.utils import getTestFilePath
from wowlint.validation.core import Severity, Issue


class TestLinter(TestCase):
    def testPassesConfig(self):
        testFile = getTestFilePath("TestLinter.wsg")
        config = {
            "HasNoCopyright": {
                "exclude": [
                    testFile
                ]
            }
        }

        linter = Linter(config=config)
        results = linter.lint(testFile)

        self.assertEqual([], results)

    def testUnknownFileExtension(self):
        linter = Linter()
        results = linter.lint(getTestFilePath("unknown.ext"))
        self.assertEqual(
            [
                Issue(Severity.INFO, "Unrecognised file extension: .ext")
            ],
            results
        )
