import requests


def get_json(url, query_dict):
    """
    Make a RESTful GET request to a URL with the provided query parameters
    """
    response = requests.get(url, params=query_dict)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        raise requests.exceptions.RequestException(
            {
                "url":          url,
                "query_params": query_dict,
                "status":       response.status_code,
                "body":         response.text
            }
        )

def find_models(base_url, **query_dict):
    return get_json(base_url + "/model", query_dict)

def find_cars(base_url, **query_dict):
    return get_json(base_url + "/car", query_dict)

def find_bookings(base_url, **query_dict):
    return get_json(base_url + "/booking", query_dict)

if __name__ == "__main__":
    base_url = "http://localhost:5000"

    print("ALL MODELS")
    for model in find_models(base_url):
        print(model)

    print("ALL CARS")
    for car in find_cars(base_url):
        print(car)

    print("findByModelName")
    for car in find_cars(base_url, model = "mini"):
        print(car)

    print("ALL BOOKINGS")
    for booking in find_bookings(base_url):
        print(booking)

    print("findByCustomer")
    for booking in find_bookings(base_url, customer = "Fred Flintstone"):
        print(booking)
