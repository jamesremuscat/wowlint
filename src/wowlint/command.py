import argparse
import os
from wowlint.linter import Linter


def main():
    parser = argparse.ArgumentParser(description='Lint and validate Words of Worship resource files.')
    parser.add_argument('file', nargs='+', help='File(s) to validate')
    args = parser.parse_args()

    issues = []

    linter = Linter()

    longestFileName = 0

    for subject in args.file:
        if os.path.isfile(subject):
            issues += linter.lint(subject)
            longestFileName = max(longestFileName, len(subject))

    for issue in issues:
        print "{:{width}}: {:8} {}".format(issue.sourceFile, issue.severity, issue.message, width=longestFileName + 2)

if __name__ == "__main__":
    main()
