import pytest
import roman


@pytest.mark.parametrize(
    "single_numeral, expected", 
    [
        ('I',     1),
        ('II',    2),
        ('III',   3),
        ('IV',    4),
        ('V',     5),
        ('IX',    9),
        ('X',    10),
        ('XX',   20),
        ('XXX',  30),
        ('XL',   40),
        ('L',    50),
        ('XC',   90),
        ('C',   100),
        ('CC',  200),
        ('CCC', 300),
        ('CD',  400),
        ('D',   500),
        ('CM',  900),
        ('M',  1000),
    ]
)


def test_single_numeral(single_numeral, expected):
    assert roman.Numeral(single_numeral) == expected


@pytest.mark.parametrize(
    "multiple_numerals, expected", 
    [
        ('XI',           11),
        ('XVI',          16),
        ('XXVI',         26),
        ('LXXXVI',       86),
        ('CCLXXXVI',    286),
        ('DCLXXXVI',    686),
        ('MMDCLXXXVI', 2686)
    ]
)


def test_multiple_numerals(multiple_numerals, expected):
    assert roman.Numeral(multiple_numerals) == expected


@pytest.mark.parametrize(
    "unrecognised_numeral, expected", 
    [
        ('xI',  'unrecognised numeral [xI]'),
        ('IIx', 'unrecognised numeral II[x]'),
        ('IiV', 'unrecognised numeral I[iV]')
    ]
)
    

def test_unrecognised_numeral(unrecognised_numeral, expected):
    assert roman.Numeral(unrecognised_numeral) == expected

    
def test_repeating_digits():
    assert roman.Numeral('MMMDCCIII') == 3703
    

@pytest.mark.parametrize(
    "bad_repetition, expected", 
    [
        ('IIII',   'bad repetition III[I]'),
        ('CVVII',  'bad repetition CV[V]II'),
        ('CLLII',  'bad repetition CL[L]II'),
        ('MDDII',  'bad repetition MD[D]II')
    ]
)


def test_bad_repetition(bad_repetition, expected):
    assert roman.Numeral(bad_repetition) == expected
    

@pytest.mark.parametrize(
    "bad_increasing_value, expected", 
    [
        ('IC',   'increasing value I[C]'),
        ('ID',   'increasing value I[D]'),
        ('IM',   'increasing value I[M]'),
        ('VX',   'increasing value V[X]'),
        ('VL',   'increasing value V[L]'),
        ('VCVI', 'increasing value V[C]VI'),
        ('VD',   'increasing value V[D]'),
        ('VMCC', 'increasing value V[M]CC'),
        ('IL',   'increasing value I[L]')
    ]
)

     
def test_bad_increasing_value(bad_increasing_value, expected):
    assert roman.Numeral(bad_increasing_value) == expected
