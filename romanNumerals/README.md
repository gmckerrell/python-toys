# [roman.py](roman.py)
A module to enable the conversion of decimal to/from roman numerals.
## Usage
```
 $ python
 >>> import roman
 >>> roman.asDecimal("MMLXIII")
 2063
 >>> roman.asNumerals(2063)
 "MMLXIII"
 >>>
```
## [example.py](example.py)
```
$ python example.py
Enter space separated values to convert to/from roman numerals.
'q' to quit

Decimals and/or numerals to convert: 1234
1234 --> MCCXXXIV

Decimals and/or numerals to convert: MCC
MCC --> 1200

Decimals and/or numerals to convert: 12 MCI
12 --> XII
MCI --> 1101

Decimals and/or numerals to convert: MCGI
*** unrecognised numeral MC[GI]

Decimals and/or numerals to convert: q
```
