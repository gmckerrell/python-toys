"""
 This module provides the means to convert
 between roman numerals and decimal.

 EXAMPLE USAGE:

 $ python
 >>> import roman
 >>> roman.asDecimal("MMLXIII")
 2063
 >>> roman.asNumerals(2063)
 "MMLXIII"
 >>>
"""

_VALUES = {
    'I':     1,
    'II':    2,
    'III':   3,
    'IV':    4,
    'V':     5,
    'IX':    9,
    'X':    10,
    'XX':   20,
    'XXX':  30,
    'XL':   40,
    'L':    50,
    'XC':   90,
    'C':   100,
    'CC':  200,
    'CCC': 300,
    'CD':  400,
    'D':   500,
    'CM':  900,
    'M':  1000,
}

_NUMERALS_ORDERED_BY_STRING_LENGTH = sorted(
    _VALUES.keys(),
    key=lambda k: len(k),
    reverse=True
)

_VALUES_ORDERED_BY_SIZE = sorted(
    _VALUES.items(),
    key=lambda item: item[1],
    reverse=True
)


def _getNumeral(string):
    for numeral in _NUMERALS_ORDERED_BY_STRING_LENGTH:
        if string.startswith(numeral):
            # remove the numeral from the string
            newString = string.replace(numeral, '', 1)
            return (numeral, newString)

    # didn't match a roman numeral!
    raise ValueError()


def asDecimal(string):
    """
    Convert a set of roman numerals into a decimal integer.
        value - a string containing the roman numerals

    RETURNS
        Integer

    RAISES
        ValueError
        - when invalid character is found
        - when invalid increasing numeral value
        - when invalid repetition of numerals
    """
    print("asDecimal(%s)" % string)

    numerals = []
    values = []
    while(string):
        try:
            # split off the next roman digit
            (numeral, string) = _getNumeral(string)
        except ValueError:
            raise ValueError("unrecognised numeral %s[%s]" % (''.join(numerals), string))

        # get the decimal value of this numeral
        value = _VALUES[numeral]

        # get the context in case of errors
        context = "%s[%s]%s" % ("".join(numerals), numeral, string)

        # cannot have a value greater than the previous one
        if (values and (value > values[-1])):
            raise ValueError("increasing value %s" % (context))

        # cannot start the next numeral with the last
        # character of the previous numeral unless it is 'M'
        if (numerals and numeral != 'M' and (numeral[0] == numerals[-1][-1])):
            raise ValueError("bad repetition %s" % (context))

        values.append(value)
        numerals.append(numeral)

    return sum(values)


def asNumerals(value):
    """
    Convert an integer into a set of roman numerals.
        value - the integer to convert

    RETURNS
        String

    RAISES
        ValueError
        - when value is out of range
    """
    if value < 1:
        raise ValueError("out of range %d" % (value))
    numerals = []
    while(value):
        for (numeral, v) in _VALUES_ORDERED_BY_SIZE:
            if v <= value:
                numerals.append(numeral)
                value -= v
                break
    return "".join(numerals)


class Numeral(int):
    def __new__(clazz, value):
        if isinstance(value, str):
            value = asDecimal(value)
        return int.__new__(clazz, value)

    def __init__(self, value):
        self.__numerals = asNumerals(self)
      
    def __repr__(self):
        return object.__repr__(self)

    def __str__(self):
        return self.__numerals;

    def __add__(self, value):
        return Numeral(int(self) + value)

    def __sub__(self, value):
        return Numeral(int(self) - value)
