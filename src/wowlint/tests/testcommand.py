from StringIO import StringIO
from unittest.case import TestCase

from wowlint.command import wowlint, getArgumentsParser


class TestCommand(TestCase):

    def runCommand(self, argsArray, expected, expectedRetVal=None):
        args = getArgumentsParser().parse_args(argsArray)
        stream = StringIO()

        retVal = wowlint(args, stream)

        if expectedRetVal:
            self.assertEqual(expectedRetVal, retVal)

        output = stream.getvalue()

        self.assertEqual(expected, output)

        stream.close()

    def testNormalUsage(self):
        expected = """src/wowlint/tests/data/TestCommand.wsg  : ERROR    HasNoCopyright No copyright details provided
src/wowlint/tests/data/TestCommand.wsg  : WARNING  TrailingComma (0:0) Line has trailing comma
1 file, 1 failed, 1 error, 1 warning
"""
        self.runCommand(
            ["src/wowlint/tests/data/TestCommand.wsg"],
            expected,
            1
        )

    def testList(self):
        expected = "src/wowlint/tests/data/TestCommand.wsg\n"
        self.runCommand(
            ["-l", "src/wowlint/tests/data/TestCommand.wsg"],
            expected,
            1
        )

    def testErrorsOnly(self):
        expected = """src/wowlint/tests/data/TestCommand.wsg  : ERROR    HasNoCopyright No copyright details provided
1 file, 1 failed, 1 error
"""
        self.runCommand(
            ["-e", "src/wowlint/tests/data/TestCommand.wsg"],
            expected,
            1
        )

    def testNoSummary(self):
        expected = """src/wowlint/tests/data/TestCommand.wsg  : ERROR    HasNoCopyright No copyright details provided
src/wowlint/tests/data/TestCommand.wsg  : WARNING  TrailingComma (0:0) Line has trailing comma
"""
        self.runCommand(
            ["-S", "src/wowlint/tests/data/TestCommand.wsg"],
            expected,
            1
        )
