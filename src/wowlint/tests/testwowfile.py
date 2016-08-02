import unittest

from wowlint.tests.utils import getTestFile
from wowlint.wowfile import Song, LicenseType, BlockType, LineType


class TestSongFile(unittest.TestCase):

    def testParseSongFile(self):
        with getTestFile("test.wsg") as f:
            song = Song.parse(f.read())

            self.assertEqual(3, song.blockcount)
            self.assertEqual("Test Author", song.author)
            self.assertEqual("Test Copyright", song.copyright)
            self.assertEqual(LicenseType.CCL, song.license.type)

            self.assertEqual(3, len(song.block))

            verse1 = song.block[0]
            self.assertEqual(BlockType.VERSE, verse1.type)

            firstLine = verse1.line[0]
            self.assertEqual("Test song, first verse, line major", firstLine.text)
            self.assertEqual(LineType.NORMAL, firstLine.type)

            secondLine = verse1.line[1]
            self.assertEqual("Test song, first verse, second line minor", secondLine.text)
            self.assertEqual(LineType.MINOR, secondLine.type)

            self.assertEqual(BlockType.CHORUS, song.block[1].type)
            self.assertEqual(BlockType.BRIDGE, song.block[2].type)
