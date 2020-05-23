import 
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

def test_single_numeral(single_numeral, expected):
    assert Numeral(single_numeral) == expected
