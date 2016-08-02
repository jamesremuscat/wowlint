from StringIO import StringIO
from unittest.case import TestCase

from wowlint.command import wowlint, getArgumentsParser


class TestCommand(TestCase):

    def testNormalUsage(self):
        args = getArgumentsParser().parse_args(["src/wowlint/tests/data/TestCommand.wsg"])
        stream = StringIO()

        retVal = wowlint(args, stream)

        self.assertEqual(1, retVal)

        output = stream.getvalue()

        expected = """src/wowlint/tests/data/TestCommand.wsg  : ERROR    HasNoCopyright No copyright details provided
src/wowlint/tests/data/TestCommand.wsg  : WARNING  TrailingComma (0:0) Line has trailing comma
1 file, 1 failed, 1 error, 1 warning
"""

        self.assertEqual(expected, output)

        stream.close()
