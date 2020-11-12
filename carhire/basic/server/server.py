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

class ModelList(Resource):
    def get(self):
        try:
            return db.find_models(conn, **flask.request.args)
        except KeyError as err:
            abort(400, message=err.args)

class Model(Resource):
    def get(self, model_id):
        try:
            return db.find_models(conn, id=model_id)[0]
        except IndexError:
            abort(404, message=f"Model '{model_id}' can't be found")

class CarList(Resource):
    def get(self):
        try:
            return db.find_cars(conn, **flask.request.args)
        except KeyError as err:
            abort(400, message=err.args)

class Car(Resource):
    def get(self, car_id):
        try:
            return db.find_cars(conn, id=car_id)[0]
        except IndexError:
            abort(404, message=f"Car '{car_id}' can't be found")

class BookingList(Resource):
    def get(self):
        try:
            return db.find_bookings(conn, **flask.request.args)
        except KeyError as err:
            abort(400, message=err.args)

class Booking(Resource):
    def get(self, booking_id):
        try:
            return db.find_bookings(conn, id=booking_id)[0]
        except IndexError:
            abort(404, message=f"Booking '{booking_id}' can't be found")

api.add_resource(ModelList,   '/model')
api.add_resource(Model,       '/model/<model_id>')
api.add_resource(CarList,     '/car')
api.add_resource(Car,         '/car/<car_id>')
api.add_resource(BookingList, '/booking')
api.add_resource(Booking,     '/booking/<booking_id>')

if __name__ == "__main__":
    app.run("localhost", port=5000)
