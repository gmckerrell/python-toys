# python-toys
some small python snippets
## [days.py](days.py)
Generates the full words for the twelve days of christmas
```
$ python days.py
On the first day of christmas
My true love gave to me
a partridge in a pear tree

On the second day of christmas
My true love gave to me
two turtle doves
and a partridge in a pear tree

On the third day of christmas
My true love gave to me
three french hens
two turtle doves
and a partridge in a pear tree

...

On the twelth day of christmas
My true love gave to me
twelve drummers drumming
eleven pipers piping
ten lords a leaping
nine ladies dancing
eight maids a milking
seven swans a swimming
six geese a laying
FIVE GOLD RINGS
four calling birds
three french hens
two turtle doves
and a partridge in a pear tree
```
## [roman.py](romanNumerals/roman.py)
A module to enable the conversion of decimal to/from roman numerals.
### Module usage
```
 $ python
 >>> import roman
 >>> roman.asDecimal("MMLXIII")
 2063
 >>> roman.asNumerals(2063)
 "MMLXIII"
 >>>
```
### Example application
```
$ python example.py
Enter space separated values to convert to/from roman numerals.
'q' to quit

Decimals and/or numerals to convert: 1234
1234 --> MCCXXXIV

Decimals and/or numerals to convert: MCC
MCC --> 1200

Decimals and/or numerals to convert: q
```
