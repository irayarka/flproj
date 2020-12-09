from flask import Blueprint, jsonify, request
import dbu
from models import Session, user_table, car_table, order_table
from schema import UserDetails, UserQuery, OrderDetails, OrderQuery, CarDetails, CarQuery, LoginData, Token, ListUsersReq, Response
from contextlib import contextmanager

api_blueprint = Blueprint('api', __name__)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    else:
        try:
            session.commit()
        except:
            session.rollback()
            raise


@api_blueprint.route("/login", methods=["POST"])
def login():
    LoginData().load(request.json)
    return jsonify(Token().dump({"token": ""}))


@api_blueprint.route("/user", methods=["GET"])
def list_users():
    with session_scope():
        args = ListUsersReq().load(request.args)
        userlist = dbu.list_users(args.get("email"), args.get("username"))
        return jsonify(UserDetails(many=True).dump(userlist))


@api_blueprint.route("/user", methods=["POST"])
def create_user():
    with session_scope():
        user_details = UserQuery().load(request.get_json(force=True))
        user = dbu.create_entry(user_table, **user_details)
        return jsonify({"id": UserDetails().dump(user)["id"]})


@api_blueprint.route("/user/<int:id>", methods=["GET"])
def user_by_id(id):
    with session_scope():
        user = dbu.get_entry_by_id(user_table, id)
        return jsonify(UserDetails().dump(user))


@api_blueprint.route("/user/<int:id>", methods=["PUT"])
def update_user(id):
    with session_scope():
        user_details = UserQuery().load(request.json)
        user = dbu.get_entry_by_id(user_table, id)
        dbu.update_entry(user, **user_details)
        return jsonify(Response().dump({"code": "200"}))


@api_blueprint.route("/user/<int:id>", methods=["DELETE"])
def delete_user(id):
    with session_scope():
        dbu.delete_entry(user_table, id)
        return jsonify(Response().dump({"code": "200"}))


@api_blueprint.route("/cars", methods=["GET"])
def get_inventory():
    with session_scope():
        cars = dbu.list_cars()
        return jsonify(CarDetails(many=True).dump(cars))


@api_blueprint.route("/cars/car/<int:carId>", methods=["GET"])
def get_car_by_id(carId):
    with session_scope():
        car = dbu.get_car_by_id(car_table, carId)
        return jsonify(CarDetails().dump(car))


@api_blueprint.route("/cars/car", methods=["POST"])
def create_car():
    with session_scope():
        car_details = CarQuery().load(request.json)
        car = dbu.create_entry(car_table, **car_details)
        return jsonify({"carId": CarDetails().dump(car)["carId"]})


@api_blueprint.route("/cars/car/<int:carId>", methods=["PUT"])
def update_car(carId):
    with session_scope():
        car_details = CarQuery().load(request.json)
        car = dbu.get_car_by_id(car_table, carId)
        dbu.update_entry(car, **car_details)
        return jsonify(Response().dump({"code": "200"}))


@api_blueprint.route("/cars/car/<int:carId>", methods=["DELETE"])
def delete_car(carId):
    with session_scope():
        dbu.delete_car(car_table, carId)
        return jsonify(Response().dump({"code": "200"}))


@api_blueprint.route("/cars/car/<int:carId>/order", methods=["POST"])
def place_order(carId):
    with session_scope():
        order_data = OrderQuery().load(request.json)
        order = dbu.create_entry(order_table,
                                 userId=order_data["userId"],
                                 carId=carId,
                                 shipDate=order_data["shipDate"],
                                 returnDate=order_data["returnDate"],
                                 status="placed",
                                 complete=False)
        return jsonify({"id": OrderDetails().dump(order)["id"]})


@api_blueprint.route("/cars/car/<int:carId>/order/<int:orderId>", methods=["GET"])
def get_order_by_id(carId, orderId):
    with session_scope():
        order = dbu.get_entry_by_id(order_table, id=orderId)
        return jsonify(OrderDetails().dump(order))


@api_blueprint.route("/cars/car/<int:carId>/order/<int:orderId>", methods=["DELETE"])
def delete_order(carId, orderId):
    with session_scope():
        dbu.delete_entry(order_table, id=orderId)
        return jsonify(Response().dump({"code": "200"}))
