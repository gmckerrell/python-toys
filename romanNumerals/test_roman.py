import pytest
import roman


@pytest.mark.parametrize(
    "good_value, expected",
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
        ('MMMDCCIII', 3703),
        # from decimal value
        (1971, 'MCMLXXI'),
        (1998, 'MCMXCVIII'),
    ]
)
def test_good_value(good_value, expected):
    assert roman.Numeral(good_value) == roman.Numeral(expected)


@pytest.mark.parametrize(
    "bad_value, expected",
    [
        # unrecognised numerals
        ('xI',  'unrecognised numeral [xI]'),
        ('IIx', 'unrecognised numeral II[x]'),
        ('IiV', 'unrecognised numeral I[iV]'),
        # bad repetition of numerals
        ('IIII',   'bad repetition III[I]'),
        ('CVVII',  'bad repetition CV[V]II'),
        ('CLLII',  'bad repetition CL[L]II'),
        ('MDDII',  'bad repetition MD[D]II'),
        # increasing numeral values
        ('IC',   'increasing value I[C]'),
        ('ID',   'increasing value I[D]'),
        ('IM',   'increasing value I[M]'),
        ('VX',   'increasing value V[X]'),
        ('VL',   'increasing value V[L]'),
        ('VCVI', 'increasing value V[C]VI'),
        ('VD',   'increasing value V[D]'),
        ('VMCC', 'increasing value V[M]CC'),
        ('IL',   'increasing value I[L]'),
        # out of range decimal values
        (-1, 'out of range -1'),
        (0,  'out of range 0'),
    ]
)
def test_bad_value(bad_value, expected):
    with pytest.raises(ValueError) as err:
        roman.Numeral(bad_value)
    assert str(err.value) == expected


def test_to_two_thousand():
    for i in range(1, 2001):
        assert roman.Numeral(
            str(
                roman.Numeral(i)
            )
        ) == i
