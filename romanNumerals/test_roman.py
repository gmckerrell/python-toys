import 
@pytest.mark.parametrize(
    "single_numeral, expected", 
    [
    ('I',.    1)
    ('II',    2),
    ('III',   3),
    ('IV',    4),
    ('V',     5),
    ('IX',    9),
    ('X',    10),
    ('XX',   20),
    ('XXX',  30),
    ('XL',   40)
    ('L',    50),
    ('XC',   90),
    ('C',   100),
    ('CC',  200),
    ('CCC', 300)
    ('CD',  400),
    ('D',   500),
    ('CM',  900),
    ('M',  1000),
    ]
)


def _checkGoodValue(value, expected):
    assert asDecimal(value) == expected
        #------------------------------------
        def _checkBadValue(self, value, expected):
            # check that this exception is raised
            with self.assertRaises(ValueError) as context:
                asDecimal(value)
            # now check the details held in the exception
            self.assertEqual(context.exception.args, ValueError(expected).args)
        
def test_single_digits():
    assert asDecimal('I') == 1
    

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
