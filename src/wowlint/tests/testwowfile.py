import os
import unittest

from wowlint.wowfile import Song, LicenseType, BlockType, LineType


def getTestFile(filename):
    path = os.path.join(os.path.dirname(__file__), "data", filename)
    return open(path, "rb")


class TestSongFile(unittest.TestCase):

    def testParseSongFile(self):
        with getTestFile("test.wsg") as f:
            song = Song.parse(f.read())

            self.assertEqual(4, song.blockcount)
            self.assertEqual("Matt Redman", song.author)
            self.assertEqual(LicenseType.CCL, song.license.type)

            self.assertEqual(4, len(song.block))

            chorus = song.block[0]
            self.assertEqual(BlockType.CHORUS, chorus.type)

            firstLine = chorus.line[0]
            self.assertEqual("Bless the Lord, O my soul", firstLine.text)
            self.assertEqual(LineType.NORMAL, firstLine.type)
