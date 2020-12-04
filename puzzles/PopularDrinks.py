"""
This problem was asked by Amazon.

At a popular bar, each customer has a set of favorite drinks,
and will happily accept any drink among this set.
For example, in the following situation, customer 0 will be
satisfied with drinks 0, 1, 3, or 6.

preferences = {
    0: [0, 1, 3, 6],
    1: [1, 4, 7],
    2: [2, 4, 7, 5],
    3: [3, 2, 5],
    4: [5, 8]
}
A lazy bartender working at this bar is trying to reduce his effort
by limiting the drink recipes he must memorize. Given a dictionary
input such as the one above, return the fewest number of drinks
he must learn in order to satisfy all customers.

For the input above, the answer would be 2, as drinks 1 and 5
will satisfy everyone.
"""

def required_drinks(preferences):
    """
    This function takes a dictionary of personal preferences in the form
    {
        PERSON_1: [DRINK_1, DRINK_2, ...],
        ...
    }
    and returns the minimum list of required drinks needed to satisfy all the
    customers in the following format
    [
        (DRINK_1, [PERSON_1, PERSON_2, ...]),
        (...),
        ...
    ]
    """
    # take a working copy
    outstanding_preferences = dict(preferences)
    drinks = []
    while(outstanding_preferences):
        drink = most_popular_drink(outstanding_preferences)
        drinks.append(drink)
        # now remove any satisfied customers
        for person in drink[1]:
            del outstanding_preferences[person]

    return drinks

def most_popular_drink(preferences):
    """
    This function takes a dictionary of personal preferences in the form
    {
        PERSON_1: [DRINK_1, DRINK_2, ...],
        ...
    }
    and identifies the most popular drink returning it as a tuple of the form
    (DRINK_1, [PERSON_1, PERSON_2, ...])
    """
    return sorted(
        drinks_from_preferences(preferences).items(),
        # sort drinks by popularity
        key = drink_popularity_weighting,
        # more popular drinks come first
        reverse = True
    )[0]

def drink_popularity_weighting(drink_details):
    """
    This function takes a tuple of drink details of the form
    (DRINK_1, [PERSON_1, PERSON_2,...])
    and returns a number representing the "weighting" of the entry.
    The weighting for a drink is defined as

    NUMBER_OF_PEOPLE * 100 + DRINK_NUMBER

    We use the drink number as a tie-break for drinks that
    have the same number of people. This means will will always
    get a repeatable result.
    """
    return len(drink_details[1]) * 100 + drink_details[0]

def drinks_from_preferences(preferences):
    """
    This function takes a dictionary of personal preferences in the form
    {
        PERSON_1: [DRINK_1, DRINK_2, ...],
        ...
    }
    and flips it to provide a dictionary of drinks that list the people
    who like them
    e.g.
    {
        DRINK_1: [PERSON_1, PERSON_2, ...],
        ...
    }
    """
    drinks = {}
    # we sort to ensure repeatable results
    for person in sorted(preferences.keys()):
        for drink in preferences[person]:
            if not drink in drinks:
                drinks[drink] = []
            drinks[drink].append(person)

    return drinks


if __name__ == "__main__":
    import unittest
    
    # define the tests
    class PopularDrinksTest(unittest.TestCase):
        def setUp(self):
            self._preferences = {
                0: [0, 1, 3, 6],
                1: [1, 4, 7],
                2: [2, 4, 7, 5],
                3: [3, 2, 5],
                4: [5, 8]
            }

        def test_drinks_from_preferences(self):
            self.assertEqual(
                drinks_from_preferences(self._preferences),
                {
                    0: [0],
                    1: [0, 1],
                    2: [2, 3],
                    3: [0, 3],
                    4: [1, 2],
                    5: [2, 3, 4],
                    6: [0],
                    7: [1, 2],
                    8: [4]
                }
            )

        def test_drink_popularity_weighting(self):
            self.assertEqual(
                drink_popularity_weighting(
                    (0, [1, 2, 3])
                ),
                300
            )
            self.assertEqual(
                drink_popularity_weighting(
                    (3, [1, 2, 3])
                ),
                303
            )
            self.assertEqual(
                drink_popularity_weighting(
                    (3, [])
                ),
                3
            )
            self.assertEqual(
                drink_popularity_weighting(
                    (2, [1, 5, 3, 4])
                ),
                402
            )

        def test_most_popular_drink(self):
            self.assertEqual(
                most_popular_drink(self._preferences),
                (5, [2, 3, 4])
            )

        def test_required_drinks(self):
            self.assertEqual(
                required_drinks(self._preferences),
                [
                    (5, [2, 3, 4]),
                    (1, [0, 1]) 
                ]
            )

    # run the tests
    unittest.main(verbosity=2)
