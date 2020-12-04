"""
This problem was asked by Airbnb.

You are given a huge list of airline ticket prices between different cities
around the world on a given day. These are all direct flights. Each element
in the list has the format (source_city, destination, price).

Consider a user who is willing to take up to k connections from their origin
city A to their destination B. Find the cheapest fare possible for this
journey and print the itinerary for that journey.

For example, our traveler wants to go from JFK to LAX with up to
3 connections, and our input flights are as follows:

[
    ('JFK', 'ATL', 150),
    ('ATL', 'SFO', 400),
    ('ORD', 'LAX', 200),
    ('LAX', 'DFW', 80),
    ('JFK', 'HKG', 800),
    ('ATL', 'ORD', 90),
    ('JFK', 'LAX', 500),
]
Due to some improbably low flight prices, the cheapest itinerary would be
JFK -> ATL -> ORD -> LAX, costing $440.
"""
CONNECTIONS = (
    ('JFK', 'ATL', 150),
    ('ATL', 'SFO', 400),
    ('ORD', 'LAX', 200),
    ('LAX', 'DFW', 80),
    ('JFK', 'HKG', 800),
    ('ATL', 'ORD', 90),
    ('JFK', 'LAX', 500),
)

def find_cheapest_route(source, destination, max_connections):
    """
    Returns the cheapest route that can be found for the constraints
    
    ([AIRPORT_1, AIRPORT_2...], TOTAL_COST)
    """
    return find_routes(source, destination, max_connections)[0]

def find_routes(source, destination, max_connections):
    """
    returns a list of possible routes for the constraints in
    ascending price order
    [
        ([AIRPORT_1, AIRPORT_2, ...], TOTAL_COST_1),
        ...
    ]
    """
    all_routes = sorted(
        recursive_search([source], destination, 0),
        key = lambda entry: entry[1]
    )
    result = []
    for route in all_routes:
        connections = len(route[0]) - 2
        if (connections <= max_connections):
            result.append(route)
    return result

def recursive_search(route, destination, cost):
    """
    route       - a list of connections
    destination - the final destination
    cost        - the current cost of this route

    Will return a list of tuples of the following format
    [
        ([AIRPORT_1, AIRPORT_2, ...], TOTAL_COST_1),
        ...
    ]
    each entry represents a possible route to the required destination
    """
    if (len(route) > 1) and (route[-1] in route[:-1]):
        # this is a circular route, do not continue searching
        return []

    routes = []
    for connection in CONNECTIONS:
        if connection[0] is route[-1]: # current airport
            next_route = list(route) # take a copy
            next_route.append(connection[1])
            
            next_cost = cost + connection[2]
            
            if connection[1] is destination:
                # job done we've found our destination
                routes.append(
                    (next_route, next_cost)
                )
            else:
                # search for a deeper route
                sub_routes = recursive_search(
                    next_route,
                    destination,
                    next_cost
                )
                for entry in sub_routes:
                    routes.append(entry)

    return routes


if __name__ == "__main__":
    import unittest
    
    # define the tests
    class CheapestFlightsTest(unittest.TestCase):

        def test_atl_to_ord(self):
            self.assertEqual(
                find_routes("ATL", "ORD", 0),
                [
                    (['ATL', 'ORD'], 90)
                ]
            )
            
        def test_jfk_to_lax_direct(self):
            self.assertEqual(
                find_routes("JFK", "LAX", 0),
                [
                    (['JFK', 'LAX'], 500)
                ]
            )

        def test_jfk_to_lax_with_one_connection(self):
            self.assertEqual(
                find_routes("JFK", "LAX", 1),
                [
                    (['JFK', 'LAX'], 500)
                ]
            )
            
        def test_jfk_to_lax_with_two_connections(self):
            self.assertEqual(
                find_routes("JFK", "LAX", 2),
                [
                    (['JFK', 'ATL', 'ORD', 'LAX'], 440),
                    (['JFK', 'LAX'], 500)
                ]
            )

        def test_atl_to_dfw_with_two_connections(self):
            self.assertEqual(
                find_routes("ATL", "DFW", 2),
                [
                    (['ATL', 'ORD', 'LAX', 'DFW'], 370)
                ]
            )

        def test_cheapest_jfk_to_lax_with_two_connections(self):
            self.assertEqual(
                find_cheapest_route("JFK", "LAX", 2),
                (['JFK', 'ATL', 'ORD', 'LAX'], 440)
            )

        def test_cheapest_jfk_to_lax_with_one_connection(self):
            self.assertEqual(
                find_cheapest_route("JFK", "LAX", 1),
                (['JFK', 'LAX'], 500)
            )
            

    # run the tests
    unittest.main(verbosity=2)
