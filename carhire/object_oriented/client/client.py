import requests


def get_json(url, params):
    """
    Make a RESTful GET request to a URL with the provided query parameters
    """
    response = requests.get(url, params=params)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        raise requests.exceptions.RequestException(
            {
                "url":    url,
                "params": params,
                "status": response.status_code,
                "body":   response.text
            }
        )

def find_models(base_url, **criteria):
    return get_json(base_url + "/model", criteria)

def find_cars(base_url, **criteria):
    return get_json(base_url + "/car", criteria)

def find_bookings(base_url, **criteria):
    return get_json(base_url + "/booking", criteria)

if __name__ == "__main__":
    base_url = "http://localhost:5000"

    print("ALL MODELS")
    for model in find_models(base_url):
        print(model)

#    print("ALL CARS")
#    for car in find_cars(base_url):
#        print(car)

#    print("findByModelName")
#    for car in find_cars(base_url, model = "mini"):
#        print(car)

    print("ALL BOOKINGS")
    for booking in find_bookings(base_url):
        print(booking)

    print("findByCustomer")
    for booking in find_bookings(base_url, customer = "Fred Flintstone"):
        print(booking)
