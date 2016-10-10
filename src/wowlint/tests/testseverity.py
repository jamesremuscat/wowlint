from unittest.case import TestCase
from wowlint.validation.core import Severity


class TestSeverity(TestCase):
    def testComparisons(self):
        self.assertTrue(Severity.ERROR > Severity.WARNING)
        self.assertTrue(Severity.WARNING >= Severity.INFO)
        self.assertTrue(Severity.INFO < Severity.WARNING)
        self.assertTrue(Severity.INFO <= Severity.FATAL)
        self.assertTrue(Severity.FATAL != Severity.WARNING)
        self.assertTrue(Severity.FATAL == Severity.FATAL)
