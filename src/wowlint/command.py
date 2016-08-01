import argparse
import os
from wowlint.linter import Linter
from wowlint.validation.core import Severity


def main():
    parser = argparse.ArgumentParser(description='Lint and validate Words of Worship resource files.')
    parser.add_argument('file', nargs='+', help='File(s) to validate')
    parser.add_argument('-e', '--errors-only', action='store_true', help='Only show errors, not warnings')
    parser.add_argument('-l', '--list', action='store_true', help='Only list files, not error details')
    args = parser.parse_args()

    issues = []

    linter = Linter()

    longestFileName = 0

    for subject in args.file:
        if os.path.isfile(subject):
            minSeverity = Severity.ERROR if args.errors_only else None
            issues += linter.lint(subject, minSeverity)
            longestFileName = max(longestFileName, len(subject))

    if args.list:
        files = []
        for f in map(lambda i: i.sourceFile, issues):  # Deduplicate maintaining ordering
            if f not in files:
                files.append(f)
        for f in files:
            print f
    else:
        for issue in issues:
            print "{:{width}}: {:8} {}".format(issue.sourceFile, issue.severity, issue.message, width=longestFileName + 2)


if __name__ == "__main__":
    main()
