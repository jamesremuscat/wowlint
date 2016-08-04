from unittest.case import TestCase

from wowlint.linter import Linter
from wowlint.tests.utils import getTestFilePath


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
