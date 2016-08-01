# wowlinter
## Linter for Words of Worship resource files

[![Build Status](https://travis-ci.org/jamesremuscat/wowlinter.svg?branch=master)](https://travis-ci.org/jamesremuscat/wowlinter)
[![Coverage Status](https://coveralls.io/repos/github/jamesremuscat/wowlinter/badge.svg?branch=master)](https://coveralls.io/github/jamesremuscat/wowlinter?branch=master)

[Words of Worship](http://www.wordsofworship.com) is a popular tool for
projecting song lyrics, liturgy and other textual media in churches and houses
of worship.

`wowlinter` aims to provide a mechanism to assure quality and consistency of
the song and liturgy resource files, by automatically verifying things like:

 - Lines start with a capital letter
 - Copyright and author information is provided
 - Lines do not have trailing punctuation

The validation criteria are unashamedly based on the house style of
[St Aldates Church](https://github.com/staldates).

## Basic usage

```shell
$ wowlint [ options ] /path/to/some/wow/files/*.wow-song
```
For help with options, run:

```shell
$ wowlint --help
```

## Limitations

Currently this project is very young, and:
 - Only song files (`.wsg` and `.wow-song`) are supported
 - There's no way to specify custom validation or disable existing rules
 - Automating the running of `wowlint` is left as an exercise for the user
 - Validation is limited

# Contributions

Contributions welcome: please fork the project and submit a pull request.
