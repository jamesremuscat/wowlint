from wowlint.validation.core import Severity, Lint
from wowlint.wowfile import LicenseType


class HasNoCopyright(Lint):
    def __init__(self):
        self.message = "No copyright details provided"
        self.severity = Severity.ERROR

    def validate(self, filename, song):
        if song.copyright == "" and (not song.license or song.license.type == LicenseType.CCL):
            return [self.create_issue(filename)]


LINTS = [
    HasNoCopyright()
]
