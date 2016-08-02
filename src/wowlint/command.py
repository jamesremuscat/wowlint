import argparse
import os
import sys

from wowlint.linter import Linter
from wowlint.validation.core import Severity


def main():
    parser = argparse.ArgumentParser(description='Lint and validate Words of Worship resource files.')
    parser.add_argument('file', nargs='+', help='File(s) to validate')
    parser.add_argument('-e', '--errors-only', action='store_true', help='Only show errors, not warnings')
    parser.add_argument('-l', '--list', action='store_true', help='Only list files, not error details')
    args = parser.parse_args()

    linter = Linter(Severity.ERROR if args.errors_only else None)

    longestFileName = 0

    highestSeverityEncountered = None

    for subject in args.file:
        if os.path.isfile(subject):
            issues = linter.lint(subject)
            if len(issues) > 0:
                highestSeverityEncountered = max(max(map(lambda i: i.severity, issues), highestSeverityEncountered))
                longestFileName = max(longestFileName, len(subject))

                if args.list:
                    print subject
                else:
                    for issue in issues:
                        print "{:{width}}: {:8} {}".format(
                            subject,
                            issue.severity,
                            issue.message,
                            width=longestFileName + 2
                        )

    if highestSeverityEncountered >= Severity.ERROR:
        sys.exit(1)


if __name__ == "__main__":
    main()
