import unittest

from wowlint.tests.utils import getTestFile
from wowlint.wowfile import LicenseType, BlockType, LineType, Resource


class TestSongFile(unittest.TestCase):

    def testParseSongFile(self):
        with getTestFile("test.wsg") as f:
            song = Resource.parse(f.read())

            self.assertEqual("Song Words", song.filetype)

            self.assertEqual(3, song.content.blockcount)
            self.assertEqual("Test Author", song.content.author)
            self.assertEqual("Test Copyright", song.content.copyright)
            self.assertEqual(LicenseType.CCL, song.content.license.type)

            self.assertEqual(3, len(song.content.block))

            verse1 = song.content.block[0]
            self.assertEqual(BlockType.VERSE, verse1.type)

            firstLine = verse1.line[0]
            self.assertEqual("Test song, first verse, line major", firstLine.text)
            self.assertEqual(LineType.NORMAL, firstLine.type)

            secondLine = verse1.line[1]
            self.assertEqual("Test song, first verse, second line minor", secondLine.text)
            self.assertEqual(LineType.MINOR, secondLine.type)

            self.assertEqual(BlockType.CHORUS, song.content.block[1].type)
            self.assertEqual(BlockType.BRIDGE, song.content.block[2].type)

    def testParseLiturgyFile(self):
        with getTestFile("test.wlt") as f:
            lit = Resource.parse(f.read())

            self.assertEqual("Liturgy", lit.filetype)
            self.assertEqual(4, lit.content.linecount)

            line1 = lit.content.line[0]
            self.assertEqual(LineType.NORMAL, line1.type)
            self.assertEqual("Test liturgy first line major", line1.text)

            line2 = lit.content.line[1]
            self.assertEqual(LineType.MINOR, line2.type)
            self.assertEqual("Test liturgy second line minor", line2.text)

            line3 = lit.content.line[2]
            self.assertEqual("", line3.text)
