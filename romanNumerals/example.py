"""
 This is an example program which uses the roman2 module.
"""
# python 2 compatability
try:
    input = raw_input
except NameError:
    pass


def isDecimal(value):
    """
    Determine whether a string can be converted into a decimal integer or not.

    value - the string to examine

    returns boolean
        - True if the string is a decimal
        - False otherwise
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def main():
    import roman

    print("Enter space separated values to convert to/from roman numerals.\n'q' to quit")
    while True:
        for value in input("\nDecimals and/or numerals to convert: ").split():
            if value == 'q':
                return
            try:
                if isDecimal(value):
                    result = roman.asNumerals(
                        int(value)
                    )
                else:
                    result = roman.asDecimal(value)
                print("%s --> %s" % (value, result))
            except ValueError as error:
                print("*** %s" % (error))


main()
