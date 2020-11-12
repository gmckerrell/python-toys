import sqlite3, os, json
import flask
from flask_restful import reqparse, abort, Api, Resource, reqparse
import db

app = flask.Flask(__name__)
api = Api(app)

dbpath = "carhire.db"
first_time = not os.path.exists(dbpath)
conn = sqlite3.connect(dbpath, check_same_thread=False)

if first_time:
    db.initialise(conn)

class DbResourceCollection(Resource):
    """
    A base class to deal with collections of resources
    """
    def get(self):
        try:
            return self.handle_get(flask.request.args)
        except KeyError as err:
            abort(400, message=err.args)

    def post(self):
        try:
            return self.handle_post(
                flask.request.get_json()
            ), 201 # CREATED
        except (TypeError, ValueError) as err:
            abort(400, message=err.args)


class DbResource(Resource):
    """
    A base class to deal with individual resource instances
    """
    def get(self, id):
        try:
            return self.handle_get(id)
        except KeyError as err:
            abort(400, message=err.args)

    def delete(self, id):
        try:
            self.handle_delete(id)
        except KeyError as err:
            pass # already gone do nothing
        
        return None, 204 # NO-CONTENT


class ModelCollection(DbResourceCollection):

    def handle_get(self, query_dict):
        return db.find_models(conn, **query_dict)

    def handle_post(self, body_dict):
        return db.create_model(conn, **body_dict)


class Model(DbResource):
    
    def handle_get(self, id):
        return db.find_models(conn, id=id)[0]

    def handle_delete(self, id):
        return db.delete_model(conn, id)


class CarCollection(DbResourceCollection):

    def handle_get(self, query_dict):
        return db.find_cars(conn, **query_dict)

    def handle_post(self, body_dict):
        return db.create_car(conn, **body_dict)


class Car(DbResource):
    
    def handle_get(self, id):
        return db.find_cars(conn, id=id)[0]

    def handle_delete(self, id):
        return db.delete_car(conn, id)


class BookingCollection(DbResourceCollection):

    def handle_get(self, query_dict):
        return db.find_bookings(conn, **query_dict)

    def handle_post(self, body_dict):
        return db.create_booking(conn, **body_dict)


class Booking(DbResource):
    
    def handle_get(self, id):
        return db.find_bookings(conn, id=id)[0]

    def handle_delete(self, id):
        return db.delete_booking(conn, id)


api.add_resource(ModelCollection,   '/model', '/model/')
api.add_resource(Model,             '/model/<id>')
api.add_resource(CarCollection,     '/car', '/car/')
api.add_resource(Car,               '/car/<id>')
api.add_resource(BookingCollection, '/booking', '/booking/')
api.add_resource(Booking,           '/booking/<id>')

if __name__ == "__main__":
    app.run("localhost", port=5000)
