from StringIO import StringIO
from unittest.case import TestCase

from wowlint.command import wowlint, getArgumentsParser
from wowlint.tests.utils import getTestFilePath


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
        path = getTestFilePath("TestCommand.wsg")
        expected = """{path}  : ERROR    HasNoCopyright No copyright details provided
{path}  : WARNING  TrailingComma (0:0) Line has trailing comma
1 file, 1 failed, 1 error, 1 warning
""".format(path=path)
        self.runCommand(
            [path],
            expected,
            1
        )

    def testList(self):
        path = getTestFilePath("TestCommand.wsg")
        expected = "{path}\n".format(path=path)
        self.runCommand(
            ["-l", path],
            expected,
            1
        )

    def testErrorsOnly(self):
        path = getTestFilePath("TestCommand.wsg")
        expected = """{path}  : ERROR    HasNoCopyright No copyright details provided
1 file, 1 failed, 1 error
""".format(path=path)
        self.runCommand(
            ["-e", path],
            expected,
            1
        )

    def testNoSummary(self):
        path = getTestFilePath("TestCommand.wsg")
        expected = """{path}  : ERROR    HasNoCopyright No copyright details provided
{path}  : WARNING  TrailingComma (0:0) Line has trailing comma
""".format(path=path)
        self.runCommand(
            ["-S", path],
            expected,
            1
        )
