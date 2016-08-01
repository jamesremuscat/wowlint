import argparse
import os
from wowlint.linter import Linter
from wowlint.validation.core import Severity


def main():
    parser = argparse.ArgumentParser(description='Lint and validate Words of Worship resource files.')
    parser.add_argument('file', nargs='+', help='File(s) to validate')
    parser.add_argument('-e', '--errors-only', help='Only show errors, not warnings')
    args = parser.parse_args()

    issues = []

    linter = Linter()

    longestFileName = 0

    for subject in args.file:
        if os.path.isfile(subject):
            issues += linter.lint(subject)
            longestFileName = max(longestFileName, len(subject))

    for issue in issues:
        if args.errors_only is None or issue.severity == Severity.ERROR:
            print "{:{width}}: {:8} {}".format(issue.sourceFile, issue.severity, issue.message, width=longestFileName + 2)

if __name__ == "__main__":
    main()
