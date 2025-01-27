# REST API

## Cars
### GET a list of all cars
```sh
curl "http://localhost:8080/api/cars" \
  -H "Accept: application/json"
```
```json
[
  {
    "id": "d958b359-556a-4d80-b5ca-13dcf9461306",
    "make": "audi",
    "model": "a1",
    "capacity": "5"
  },
  {
    "id": "73d77597-87bd-47be-939d-56781f55fa05",
    "make": "audi",
    "model": "q5",
    "capacity": "5"
  },
  {
    "id": "563838e3-3391-43c7-88bb-22bf84fd3820",
    "make": "vw",
    "model": "up",
    "capacity": "3",
    "available": "yes"
  }
]
```
### GET a list of cars that satisfy search criteria

You can specify query parameters for any of the car attributes, to narrow the results.
```sh
curl "http://localhost:8080/api/cars?make=audi&capacity=5" \
  -H "Accept: application/json"
```
```json
[
  {
    "id": "d958b359-556a-4d80-b5ca-13dcf9461306",
    "make": "audi",
    "model": "a1",
    "capacity": "5"
  },
  {
    "id": "73d77597-87bd-47be-939d-56781f55fa05",
    "make": "audi",
    "model": "q5",
    "capacity": "5"
  }
]
```

### GET details for a specific car
```sh
curl "http://localhost:8080/api/cars/d958b359-556a-4d80-b5ca-13dcf9461306" \
  -H "Accept: application/json"
```
```json
{
  "id": "d958b359-556a-4d80-b5ca-13dcf9461306",
  "make": "audi",
  "model": "a1",
  "capacity": "5"
}
```
