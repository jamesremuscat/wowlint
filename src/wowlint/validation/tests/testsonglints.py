from unittest.case import TestCase

from wowlint.tests.utils import getTestFile
from wowlint.validation.core import Severity, Issue
from wowlint.validation.songs import HasNoCopyright, HasNoAuthor, AllMinorWords, NoInitialCapital, TrailingComma
from wowlint.wowfile import Resource


class TestSongLints(TestCase):

    def runTest(self, clazz, testFile, expected):
        with getTestFile(testFile, __file__) as songFile:
            results = clazz().validate(Resource.parse(songFile.read()))

            self.assertEqual(expected, results)

    def testHasNoCopyright(self):
        self.runTest(HasNoCopyright, "NoCopyright.wsg", [
            Issue(Severity.ERROR, "HasNoCopyright No copyright details provided")
        ])

        self.runTest(HasNoCopyright, "NoCopyrightButOK.wsg", [])

    def testHasNoAuthor(self):
        self.runTest(HasNoAuthor, "NoAuthor.wsg", [
            Issue(Severity.ERROR, "HasNoAuthor No author provided")
        ])

    def testAllMinorWords(self):
        self.runTest(AllMinorWords, "AllMinorWords.wsg", [
            Issue(Severity.WARNING, "AllMinorWords Entirely uses minor words")
        ])

    def testNoInitialCapital(self):
        self.runTest(NoInitialCapital, "NoInitialCapital.wsg", [
            Issue(Severity.WARNING, "NoInitialCapital (0:0) Line does not start with a capital letter"),
            Issue(Severity.WARNING, "NoInitialCapital (1:1) Line does not start with a capital letter")
        ])

    def testTrailingCommas(self):
        self.runTest(TrailingComma, "TrailingCommas.wsg", [
            Issue(Severity.WARNING, "TrailingComma (0:0) Line has trailing comma"),
            Issue(Severity.WARNING, "TrailingComma (1:1) Line has trailing comma")
        ])
