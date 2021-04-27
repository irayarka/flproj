from flask import Blueprint, jsonify, request
import dbu
from models import Session, user_table, car_table, order_table
from schema import UserDetails, UserQuery, OrderDetails, OrderQuery, CarDetails, CarQuery, LoginData, \
    ListUsersReq, Response
from contextlib import contextmanager
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
import datetime
import bcrypt

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


@api_blueprint.route("/", methods=["GET"])
def start():
    return jsonify(Started="true")


@api_blueprint.route("/login", methods=["POST"])
def login():
    from app import bcrypt
    data = LoginData().load(request.json)
    if data:
        user = dbu.get_entry_by_username(user_table, username=data["username"])
        hpw = bcrypt.generate_password_hash(data["password"])
        if not user:
            return jsonify({"message": "Couldn't find user!"})
        if bcrypt.check_password_hash(hpw, data["password"]):
            access_token = create_access_token(identity=data["username"], expires_delta=datetime.timedelta(days=365))
            return jsonify(access_token=access_token, id=user.id), 200
    #     elif not data["password"] == user.password:
    #         return jsonify({"message": "Wrong pass!", "data pass": data["password"], "user pass": user.password})
    # elif not data:
    #     return jsonify({"message": "Wrong data!"})


@api_blueprint.route("/user", methods=["GET"])
@jwt_required()
def list_users():
    with session_scope():
        current_user = get_jwt_identity()
        user = dbu.get_entry_by_username(user_table, current_user)
        if user.admin:
            args = ListUsersReq().load(request.args)
            userlist = dbu.list_users(args.get("email"), args.get("username"))
            return jsonify(UserDetails(many=True).dump(userlist))
        else:
            return jsonify(code=401, type='UNAUTHORIZED_ACCESS'), 401


@api_blueprint.route("/user", methods=["POST"])
def create_user():
    with session_scope():
        from app import bcrypt
        user_details = UserQuery().load(request.get_json(force=True))
        user_details["password"] = bcrypt.generate_password_hash(user_details["password"]).decode('UTF-8')
        user = dbu.create_entry(user_table, **user_details)
        access_token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(days=365))
        return jsonify(access_token=access_token, id=UserDetails().dump(user)["id"]), 200


@api_blueprint.route("/user/<int:id>", methods=["GET"])
@jwt_required()
def user_by_id(id):
    with session_scope():
        current_user = get_jwt_identity()
        user = dbu.get_entry_by_username(user_table, current_user)
        if user.admin:
            user = dbu.get_entry_by_id(user_table, id)
            return jsonify(UserDetails().dump(user))
        else:
            return jsonify(code=401, type="UNAUTHORIZED_ACCESS"), 401


@api_blueprint.route("/user/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    with session_scope():
        current_user = get_jwt_identity()
        user = dbu.get_entry_by_username(user_table, current_user)
        if user.admin or user.id == id:
            user_details = UserQuery().load(request.json)
            user = dbu.get_entry_by_id(user_table, id)
            dbu.update_entry(user, **user_details)
            return jsonify(Response().dump({"code": "200"}))
        else:
            return jsonify(code=401, type="UNAUTHORIZED_ACCESS"), 401


@api_blueprint.route("/user/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    with session_scope():
        current_user = get_jwt_identity()
        user = dbu.get_entry_by_username(user_table, current_user)
        if user.admin or user.id == id:
            dbu.delete_entry(user_table, id)
            return jsonify(Response().dump({"code": "200"}))
        else:
            return jsonify(code=401, type="UNAUTHORIZED_ACCESS"), 401


@api_blueprint.route("/cars", methods=["GET"])
@jwt_required()
def get_inventory():
    with session_scope():
        cars = dbu.list_cars()
        return jsonify(CarDetails(many=True).dump(cars))


@api_blueprint.route("/cars/car/<int:carId>", methods=["GET"])
@jwt_required()
def get_car_by_id(carId):
    with session_scope():
        car = dbu.get_car_by_id(car_table, carId)
        return jsonify(CarDetails().dump(car))


@api_blueprint.route("/cars/car", methods=["POST"])
@jwt_required()
def create_car():
    with session_scope():
        current_user = get_jwt_identity()
        user = dbu.get_entry_by_username(user_table, current_user)
        if user.admin:
            car_details = CarQuery().load(request.json)
            car = dbu.create_entry(car_table, **car_details)
            return jsonify({"carId": CarDetails().dump(car)["carId"]})
        else:
            return jsonify(code=401, type="UNAUTHORIZED_ACCESS"), 401


@api_blueprint.route("/cars/car/<int:carId>", methods=["PUT"])
@jwt_required()
def update_car(carId):
    with session_scope():
        current_user = get_jwt_identity()
        user = dbu.get_entry_by_username(user_table, current_user)
        if user.admin:
            car_details = CarQuery().load(request.json)
            car = dbu.get_car_by_id(car_table, carId)
            dbu.update_entry(car, **car_details)
            return jsonify(Response().dump({"code": "200"}))
        else:
            return jsonify(code=401, type="UNAUTHORIZED_ACCESS"), 401


@api_blueprint.route("/cars/car/<int:carId>", methods=["DELETE"])
@jwt_required()
def delete_car(carId):
    with session_scope():
        current_user = get_jwt_identity()
        user = dbu.get_entry_by_username(user_table, current_user)
        if user.admin:
            dbu.delete_car(car_table, carId)
            return jsonify(Response().dump({"code": "200"}))
        else:
            return jsonify(code=401, type="UNAUTHORIZED_ACCESS"), 401


@api_blueprint.route("/cars/car/<int:carId>/order", methods=["POST"])
@jwt_required()
def place_order(carId):
    with session_scope():
        current_user = get_jwt_identity()
        user = dbu.get_entry_by_username(user_table, current_user)
        if user:
            order_data = OrderQuery().load(request.json)
            order = dbu.create_entry(order_table,
                                     userId=user.id,
                                     carId=carId,
                                     shipDate=order_data["shipDate"],
                                     returnDate=order_data["returnDate"],
                                     status="placed",
                                     complete=False)
            return jsonify({"id": OrderDetails().dump(order)["id"]})
        else:
            return jsonify(code=401, type="UNAUTHORIZED_ACCESS"), 401


@api_blueprint.route("/orders", methods=["GET"])
@jwt_required()
def get_orders():
    with session_scope():
        current_user = get_jwt_identity()
        user = dbu.get_entry_by_username(user_table, current_user)
        if user.admin:
            orders = dbu.list_orders()
            return jsonify(OrderDetails(many=True).dump(orders))
        else:
            return jsonify(code=401, type="UNAUTHORIZED_ACCESS"), 401


@api_blueprint.route("/cars/car/<int:carId>/order/<int:orderId>", methods=["GET"])
@jwt_required()
def get_order_by_id(carId, orderId):
    with session_scope():
        current_user = get_jwt_identity()
        user = dbu.get_entry_by_username(user_table, current_user)
        if user:
            order = dbu.get_entry_by_id(order_table, id=orderId)
            return jsonify(OrderDetails().dump(order))
        else:
            return jsonify(code=401, type="UNAUTHORIZED_ACCESS"), 401


@api_blueprint.route("/cars/car/<int:carId>/order/<int:orderId>", methods=["DELETE"])
@jwt_required()
def delete_order(carId, orderId):
    with session_scope():
        dbu.delete_entry(order_table, id=orderId)
        return jsonify(Response().dump({"code": "200"}))
