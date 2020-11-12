# Basic example
This version tries to avoid using too much object oriented code; keeping to more simple functions

## Server
The server code provides a RESTful web service for the access and manipulation of the resources associated with the carhire database.
[`server/db.py`](server/db.py) provides the core database access and control, exposing the various actions as functions within the `db` module.

_Running this python module by itself will drop, create and fill out some default values for the database._

### Prerequisites
`python -m pip install flask_restful`

This installs the python packages that the [`server/server.py`](server/server.py) code uses to provide the web service.

_NB. You will need to have created the carhire.db database before running this._ (see above)

## Client
The client code provides similar functions as the db interface, but the implementation talks to the remote web service (if running) to perform the tasks rather than to a local database.
### Prerequisites
`python -m pip install requests`

This installs the python packages that the [`client/client.py`](client/client.py) code uses to perform REST requests.

## From a Browser
You can also query the web service yourself from a browser.
### retrieve list of all models
[`http://localhost:5000/model`](http://localhost:5000/model)

### retrieve list of all cars
[`http://localhost:5000/car`](http://localhost:5000/car)

### retrieve list of all bookings
[`http://localhost:5000/booking`](http://localhost:5000/booking)

### retrieve list of all red cars
[`http://localhost:5000/booking?color=red`](http://localhost:5000/booking?color=red)

### find specific booking
[`http://localhost:5000/booking/3`](http://localhost:5000/booking/3)

### find all bookings of 'mini'
[`http://localhost:5000/booking?model=mini`](http://localhost:5000/booking?model=mini)

### bookings with a customer name containing 'rub'
[`http://localhost:5000/booking?customer=%rub%`](http://localhost:5000/booking?customer=%rub%)


