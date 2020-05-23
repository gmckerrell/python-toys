"""
 This module provides the means to convert
 between roman numerala and decimal.

 EXAMPLE USAGE:

 $ python
 >>> import roman
 >>> roman.asDecimal("MMLXIII")
 2063
 >>> roman.asNumerals(2063)
 "MMLXIII"
 >>> 
 
"""
#----------------------------------------
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
#----------------------------------------
_NUMERALS_ORDERED_BY_STRING_LENGTH = sorted(
    _VALUES.keys(), 
    key      = lambda k: len(k),
    reverse  = True
)
#----------------------------------------
_VALUES_ORDERED_BY_SIZE = sorted(
    _VALUES.items(),
    key     = lambda item: item[1],
    reverse = True
)
#----------------------------------------
def _getNumeral(string):
    for numeral in _NUMERALS_ORDERED_BY_STRING_LENGTH:
        if string.startswith(numeral):
            # remove the numeral from the string
            newString = string.replace(numeral, '', 1)
            return (numeral, newString)

    # didn't match a roman numeral!
    raise ValueError()
#----------------------------------------
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
    numerals = []
    values = []
    while(string):
        try:
            # split off the next roman digit
            (numeral, string) = _getNumeral(string)
        except ValueError:
            raise ValueError("unrecognised numeral %s[%s]"%(''.join(numerals), string))

        # get the decimal value of this numeral
        value = _VALUES[numeral]

        # get the context in case of errors
        context = "%s[%s]%s"%("".join(numerals), numeral, string)

        # cannot have a value greater than the previous one
        if (values and (value > values[-1])):
            raise ValueError("increasing value %s"%(context))

        # cannot start the next numeral with the last
        # character of the previous numeral unless it is 'M'
        if (numerals and numeral != 'M' and (numeral[0] == numerals[-1][-1])):
            raise ValueError("bad repetition %s"%(context))

        values.append(value)
        numerals.append(numeral)

    return sum(values)
#---------------------------------------- 
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
        raise ValueError("out of range %d"%(value))
    numerals=[]
    while(value):
        for (numeral, v) in _VALUES_ORDERED_BY_SIZE:
            if v <= value:
                numerals.append(numeral)
                value -= v
                break
    return "".join(numerals)

class Numeral(int):
    def __call__(value):
        return int.new(
            Numeral,
            asDecimal(value)
        )
    def __repr__(self):
        return object.__repr__(self)

    def __str__(self):
        return asNumeral(self)
        
    def __add__(self, value):
        return Numeral(int(self) + value)
        
    def __sub__(self, value):
        return Numeral(int(self) - value)

#----------------------------------------
# UNITTESTS
#----------------------------------------
if __name__ == '__main__':
    import unittest

    #----------------------------------------
    class TestAsDecimal(unittest.TestCase):
        #------------------------------------
        def _checkGoodValue(self, value, expected):
            self.assertEqual(asDecimal(value), expected)
        #------------------------------------
        def _checkBadValue(self, value, expected):
            # check that this exception is raised
            with self.assertRaises(ValueError) as context:
                asDecimal(value)
            # now check the details held in the exception
            self.assertEqual(context.exception.args, ValueError(expected).args)
        #------------------------------------
        def test_single_digits(self):
            self._checkGoodValue('I',     1)
            self._checkGoodValue('II',    2)
            self._checkGoodValue('III',   3)
            self._checkGoodValue('IV',    4)
            self._checkGoodValue('V',     5)
            self._checkGoodValue('IX',    9)
            self._checkGoodValue('X',    10)
            self._checkGoodValue('XX',   20)
            self._checkGoodValue('XXX',  30)
            self._checkGoodValue('XL',   40)
            self._checkGoodValue('L',    50)
            self._checkGoodValue('XC',   90)
            self._checkGoodValue('C',   100)
            self._checkGoodValue('CC',  200)
            self._checkGoodValue('CCC', 300)
            self._checkGoodValue('CD',  400)
            self._checkGoodValue('D',   500)
            self._checkGoodValue('CM',  900)
            self._checkGoodValue('M',  1000)
        #------------------------------------
        def test_multiple_digits(self):
            self._checkGoodValue('XI',           11)
            self._checkGoodValue('XVI',          16)
            self._checkGoodValue('XXVI',         26)
            self._checkGoodValue('LXXXVI',       86)
            self._checkGoodValue('CCLXXXVI',    286)
            self._checkGoodValue('DCLXXXVI',    686)
            self._checkGoodValue('MMDCLXXXVI', 2686)
        #------------------------------------
        def test_valid_repeating_digits(self):
            self._checkGoodValue('MMMDCCIII', 3703)
        #------------------------------------
        def test_bad_digits(self):
            self._checkBadValue('xI',  'unrecognised numeral [xI]')
            self._checkBadValue('IIx', 'unrecognised numeral II[x]')
            self._checkBadValue('IiV', 'unrecognised numeral I[iV]')
        #------------------------------------
        def test_bad_increasing_value(self):
            self._checkBadValue('IL',   'increasing value I[L]')
            self._checkBadValue('IC',   'increasing value I[C]')
            self._checkBadValue('ID',   'increasing value I[D]')
            self._checkBadValue('IM',   'increasing value I[M]')
            self._checkBadValue('VX',   'increasing value V[X]')
            self._checkBadValue('VL',   'increasing value V[L]')
            self._checkBadValue('VCVI', 'increasing value V[C]VI')
            self._checkBadValue('VD',   'increasing value V[D]')
            self._checkBadValue('VMCC', 'increasing value V[M]CC')
        #------------------------------------
        def test_bad_repeating_values(self):
            self._checkBadValue('IIII',   'bad repetition III[I]')
            self._checkBadValue('CVVII',  'bad repetition CV[V]II')
            self._checkBadValue('CLLII',  'bad repetition CL[L]II')
            self._checkBadValue('MDDII',  'bad repetition MD[D]II')
        #------------------------------------
     #----------------------------------------
    class TestAsNumerals(unittest.TestCase):
        #------------------------------------
        def _checkGoodValue(self, value, expected):
            self.assertEqual(asNumerals(value), expected)
        #------------------------------------
        def _checkBadValue(self, value, expected):
            # check that this exception is raised
            with self.assertRaises(ValueError) as context:
                asNumerals(value)
            # now check the details held in the exception
            self.assertEqual(context.exception.args, ValueError(expected).args)
        #------------------------------------
        def test_good_values(self):
                self._checkGoodValue(1971, "MCMLXXI")
                self._checkGoodValue(1998, "MCMXCVIII")
        #------------------------------------
        def test_out_of_range(self):
                self._checkBadValue(-1, "out of range -1")
                self._checkBadValue(0,  "out of range 0")
        #------------------------------------
        def test_to_two_thousand(self):
            print()
            for i in range(1,2001):
                n = asNumerals(i)
                self.assertEqual(
                    asDecimal(n),
                    i
                )
        #------------------------------------
    unittest.main()
#----------------------------------------
