# REST API

The API provides details for the following entities
`cars`, `customers`, `bookings`

Which can be accessed under the `http:localhost:8080/api/{ENTITY}` URL
## Entity Attributes
### Cars
```json
{
  "id": "d958b359-556a-4d80-b5ca-13dcf9461306",
  "make": "audi",
  "model": "a1",
  "capacity": "5"
}
```
### Customers
```json
{
    "id": "14f4d38b-7789-4917-8cec-ddc6eebe648a",
    "firstname": "jacob",
    "surname": "mckerrell",
    "email": "jacobmckerrell@gmail.com"
  }
```

### Bookings
```json
{
    "id": "0e7752a7-283c-49d2-a29e-40485a8478ed",
    "customerid": "83feda52-8725-4b76-bf7d-b040141882f9",
    "carid": "73d77597-87bd-47be-939d-56781f55fa05",
    "date": "2025-01-28"
}
```

## Some examples using cars
### GET a list of entities
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
### GET a list of entities that satisfy search criteria

You can specify query parameters for any of the attributes, to narrow the results.
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

### GET details for a specific entity
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

### Create a new entity
