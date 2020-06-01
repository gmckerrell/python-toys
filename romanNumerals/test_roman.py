import pytest
import roman


@pytest.mark.parametrize(
    "good_numeral, expected", 
    [
        # single numerals
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
        # multiple numerals
        ('XI',           11),
        ('XVI',          16),
        ('XXVI',         26),
        ('LXXXVI',       86),
        ('CCLXXXVI',    286),
        ('DCLXXXVI',    686),
        ('MMDCLXXXVI', 2686),
        # repeating digits
        ('MMMDCCIII'), 3703),
    ]
)


def test_good_numeral(good_numeral, expected):
    assert roman.Numeral(good_numeral) == expected


@pytest.mark.parametrize(
    "bad_numeral, expected", 
    [
        ('xI',  'unrecognised numeral [xI]'),
        ('IIx', 'unrecognised numeral II[x]'),
        ('IiV', 'unrecognised numeral I[iV]'),
        ('IIII',   'bad repetition III[I]'),
        ('CVVII',  'bad repetition CV[V]II'),
        ('CLLII',  'bad repetition CL[L]II'),
        ('MDDII',  'bad repetition MD[D]II'),
        ('IC',   'increasing value I[C]'),
        ('ID',   'increasing value I[D]'),
        ('IM',   'increasing value I[M]'),
        ('VX',   'increasing value V[X]'),
        ('VL',   'increasing value V[L]'),
        ('VCVI', 'increasing value V[C]VI'),
        ('VD',   'increasing value V[D]'),
        ('VMCC', 'increasing value V[M]CC'),
        ('IL',   'increasing value I[L]'),
    ]
)
    

def test_bad_numeral(bad_numeral, expected):
    with pytest.raises(ValueError) as err:
        roman.Numeral(bad_numeral)
    assert str(err.value) == expected
