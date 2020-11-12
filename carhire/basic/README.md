# Basic example
This version tries to avoid using too much object oriented code; keeping to more simple functions

## Server
The server code provides a RESTful web service for the access and manipulation of the resources associated with the carhire database.
[`server/db.py`](server/db.py) provides the core database access and control, exposing the various actions as functions within the `db` module.

### Prerequisites
`python -m pip install flask_restful`
This installs the python packages that the [`server/server.py`](server/server.py) code uses to provide the web service.


## Client
The client code ([client/client.py](client/client.py)) simply calls the Web service (when running) provides the same functions as the db interface, but the implementation talks to the web service (if running) to perform the tasks.
