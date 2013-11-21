#!/usr/bin/python2
from pyparsing import *


def baculaParser(dir_config_file):

    LBRACE, RBRACE, EQUALS, HASH = map(Suppress, '{}=#')

    comment = HASH + Optional(restOfLine)
    strip = lambda t: t[0].strip(' "')

    SecName = Word(alphanums) + Optional(Suppress(comment))
    NONEQUALS = "".join(
        [c for c in srange('[a-zA-Z_]') if c != "="]
    ) + " \t"
    NONEQUALSEXT = "".join(
        [c for c in srange('[a-zA-Z0-9_"./]') if c != "="]
    ) + " \t"

    lineWithoutComment = restOfLine.setParseAction(
        lambda t: ((t[0].partition('#'))[0]).strip(' "')
    )

    keyDefEQ = (
        Word(NONEQUALS).setParseAction(strip) + EQUALS
        + Word(NONEQUALSEXT).setParseAction(strip) + EQUALS
        + lineWithoutComment
    )
    keyDefQuote = (
        Word(NONEQUALS).setParseAction(strip) + EQUALS
        + Regex(r'"[a-zA-Z0-9.-_]*"').setParseAction(lambda t: t[0].strip('"'))
    )
    keyDef = (
        Word(NONEQUALS).setParseAction(strip) + EQUALS
        + lineWithoutComment
    )
    keyList = delimitedList(keyDefQuote, delim=';')

    baculaObject = Forward()
    baculaDef = Forward()
    baculaSec = Forward()

    incFile = lambda t: baculaSec.parseFile(t[0])

    incDef = (Literal('@').suppress() + restOfLine).setParseAction(incFile)

    baculaSec << Dict(ZeroOrMore(
        Group(keyDefEQ | keyList | keyDef | baculaDef) | incDef
    ))
    baculaDef << SecName + LBRACE + Optional(baculaSec) + RBRACE
    baculaObject << Dict(ZeroOrMore(Group(baculaDef) | incDef))

    baculaObject.ignore(comment)

    return baculaObject.parseFile(dir_config_file)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='This script parse bacula director config to python dictionary.')
    parser.add_argument('filename',
             help='path to filename bacula-dir.conf') 
    args = parser.parse_args()
    results = baculaParser(args.filename)
    import pprint
    pprint.pprint(results.asList())

if __name__ == "__main__":
    main()
