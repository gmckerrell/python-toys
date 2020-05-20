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
