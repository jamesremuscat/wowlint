from unittest.case import TestCase

from wowlint.tests.utils import getTestFile
from wowlint.validation.core import Severity, Issue
from wowlint.validation.songs import HasNoCopyright
from wowlint.wowfile import Song


class TestSongLints(TestCase):

    def testHasNoCopyright(self):
        with getTestFile("NoCopyright.wsg", __file__) as songFile:
            results = HasNoCopyright().validate("test", Song.parse(songFile.read()))

            i = Issue(Severity.ERROR, "test", "HasNoCopyright No copyright details provided")
            self.assertEqual([i], results)
