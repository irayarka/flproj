from flask import url_for, jsonify
from flask_testing import TestCase
from flask_bcrypt import generate_password_hash
from unittest.mock import ANY
import unittest
from app import app
import dbu
from models import user_table, car_table, order_table, engine, Base, Session


class BaseTC(TestCase):
    def setUp(self):
        super().setUp()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        self.admin_login_data = {
            "username": "admin",
            "password": "1234"
        }

        self.admin_data = {
            "username": "admin",
            "firstName": "Name",
            "lastName": "Surname",
            "email": "email@gmail.com",
            "password": "1234",
            "phone": "1234",
            "admin": True
        }

        self.admin_data_pass = {
            **self.admin_data,
            "password": generate_password_hash(self.admin_data["password"]),
        }

        self.user_1_data = {
            "username": "user1",
            "firstName": "Name1",
            "lastName": "Surname1",
            "email": "email@gmail.com",
            "password": "1234",
            "phone": "1234",
            "admin": False
        }
        self.user_1_data_pass = {
            **self.user_1_data,
            "password": generate_password_hash(self.user_1_data["password"]),
        }
        self.user_1_login_data = {
            "username": self.user_1_data["username"],
            "password": self.user_1_data["password"],
        }

        self.user_2_data = {
            "username": "user2",
            "firstName": "Name2",
            "lastName": "Surname2",
            "email": "email@gmail.com",
            "password": "1234",
            "phone": "1234",
            "admin": False
        }
        self.user_2_data_pass = {
            **self.user_2_data,
            "password": generate_password_hash(self.user_2_data["password"]),
        }
        self.user_2_login_data = {
            "username": self.user_2_data["username"],
            "password": self.user_2_data["password"],
        }

        self.car_1_data = {
            "name": "BMW",
            "price": 1000.0
        }

        self.car_2_data = {
            "name": "Tesla",
            "price": 2500.0
        }

        self.order_1_data = {
            "shipDate": "2020-12-27",
            "returnDate": "2020-12-30",
            "complete": False,
            "status": "placed"
        }

        self.order_2_data = {
            "shipDate": "2020-12-26",
            "returnDate": "2020-12-31",
            "complete": False,
            "status": "placed"
        }

    def tearDown(self):
        Session().close()

    def create_app(self):
        return app

    def get_auth_headers(self, login_data):
        resp = self.client.post(url_for("api.login"), json=login_data)
        token = resp.json["access_token"]
        return {'Authorization': f'Bearer {token}'}


class TestAuthentication(BaseTC):
    def test_login(self):
        dbu.create_entry(user_table, **self.admin_data_pass)
        resp = self.client.post(url_for("api.login"), json=self.admin_login_data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"access_token": ANY, "id": ANY})


class TestListUsers(BaseTC):
    def test_list_users(self):
        dbu.create_entry(user_table, **self.admin_data_pass)
        dbu.create_entry(user_table, **self.user_1_data_pass)
        dbu.create_entry(user_table, **self.user_2_data_pass)

        resp = self.client.get(
            url_for("api.list_users"),
            headers=self.get_auth_headers(self.admin_login_data),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, [
            {
                'id': ANY,
                'username': self.admin_data['username'],
                'firstName': self.admin_data['firstName'],
                'lastName': self.admin_data['lastName'],
                'email': self.admin_data['email'],
                'phone': self.admin_data['phone'],
                'admin': self.admin_data['admin']
            },
            {
                'id': ANY,
                'username': self.user_1_data['username'],
                'firstName': self.user_1_data['firstName'],
                'lastName': self.user_1_data['lastName'],
                'email': self.user_1_data['email'],
                'phone': self.user_1_data['phone'],
                'admin': self.user_1_data['admin']
            },
            {
                'id': ANY,
                'username': self.user_2_data['username'],
                'firstName': self.user_2_data['firstName'],
                'lastName': self.user_2_data['lastName'],
                'email': self.user_2_data['email'],
                'phone': self.user_2_data['phone'],
                'admin': self.user_2_data['admin']
            }
        ])

    def test_unauthorized(self):
        resp = self.client.get(url_for("api.list_users"))
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'msg': 'Missing Authorization Header'
        })

    def test_not_admin(self):
        dbu.create_entry(user_table, **self.user_1_data_pass)

        resp = self.client.get(
            url_for("api.list_users"),
            headers=self.get_auth_headers(self.user_1_login_data),
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'UNAUTHORIZED_ACCESS',
        })


class TestCreateUser(BaseTC):
    def test_create_user(self):
        resp = self.client.post(
            url_for("api.create_user"),
            json=self.user_1_data
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"access_token": ANY, "id": ANY})
        self.assertTrue(
            Session().query(user_table).filter_by(username=self.user_1_data['username']).first()
        )


class TestGetUser(BaseTC):
    def setUp(self):
        super().setUp()
        self.user = dbu.create_entry(user_table, **self.user_1_data_pass)
        self.admin = dbu.create_entry(user_table, **self.admin_data_pass)

    def test_get_user(self):
        resp = self.client.get(
            url_for("api.user_by_id", id=self.user.id),
            headers=self.get_auth_headers(self.admin_login_data)
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'id': self.user.id,
            'username': self.user_1_data['username'],
            'firstName': self.user_1_data['firstName'],
            'lastName': self.user_1_data['lastName'],
            'email': self.user_1_data['email'],
            'phone': self.user_1_data['phone'],
            'admin': self.user_1_data['admin']
        })

    def test_unauthorized(self):
        resp = self.client.get(url_for("api.user_by_id", id=self.user.id))
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'msg': 'Missing Authorization Header'
        })

    def test_not_admin(self):
        resp = self.client.get(
            url_for("api.user_by_id", id=self.user.id),
            headers=self.get_auth_headers(self.user_1_login_data),
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'UNAUTHORIZED_ACCESS',
        })


class TestUpdateUser(BaseTC):
    def setUp(self):
        super().setUp()
        self.user_1 = dbu.create_entry(user_table, **self.user_1_data_pass)
        self.user_2 = dbu.create_entry(user_table, **self.user_2_data_pass)
        self.admin = dbu.create_entry(user_table, **self.admin_data_pass)

    def test_update_user(self):
        resp = self.client.put(
            url_for("api.update_user", id=self.user_1.id),
            json={
                **self.user_1_data,
                "firstName": "UpdatedFirstName"
            },
            headers=self.get_auth_headers(self.admin_login_data),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'code': 200,
            'type': 'OK',
        })
        self.assertTrue(
            Session().query(user_table).filter_by(firstName='UpdatedFirstName').first()
        )

    def test_unauthorized(self):
        resp = self.client.put(
            url_for("api.update_user", id=self.user_1.id),
            json={
                **self.user_1_data,
                "firstName": "UpdatedFirstName"
            },
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'msg': 'Missing Authorization Header'
        })
        self.assertFalse(
            Session().query(user_table).filter_by(firstName='UpdatedFirstName').one_or_none()
        )

    def test_self_update(self):
        resp = self.client.put(
            url_for("api.update_user", id=self.user_1.id),
            json={
                **self.user_1_data,
                "firstName": "UpdatedFirstName"
            },
            headers=self.get_auth_headers(self.user_1_login_data),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'code': 200,
            'type': 'OK',
        })
        self.assertTrue(
            Session().query(user_table).filter_by(firstName='UpdatedFirstName').first()
        )

    def test_update_another_user(self):
        resp = self.client.put(
            url_for("api.update_user", id=self.user_2.id),
            json={
                **self.user_2_data,
                "firstName": "UpdatedFirstName"
            },
            headers=self.get_auth_headers(self.user_1_login_data),
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'UNAUTHORIZED_ACCESS',
        })
        self.assertFalse(
            Session().query(user_table).filter_by(firstName='UpdatedFirstName').one_or_none()
        )


class TestDeleteUser(BaseTC):
    def setUp(self):
        super().setUp()
        self.user_1 = dbu.create_entry(user_table, **self.user_1_data_pass)
        self.user_2 = dbu.create_entry(user_table, **self.user_2_data_pass)
        self.admin = dbu.create_entry(user_table, **self.admin_data_pass)

    def test_delete_user(self):
        resp = self.client.delete(
            url_for("api.delete_user", id=self.user_1.id),
            headers=self.get_auth_headers(self.admin_login_data),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'code': 200,
            'type': 'OK',
        })
        self.assertFalse(
            Session().query(user_table).filter_by(id=self.user_1.id).one_or_none()
        )

    def test_unauthorized(self):
        resp = self.client.delete(url_for("api.delete_user", id=self.user_1.id))

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'msg': 'Missing Authorization Header'
        })
        self.assertTrue(
            Session().query(user_table).filter_by(id=self.user_1.id).one_or_none()
        )

    def test_self_delete(self):
        resp = self.client.delete(
            url_for("api.delete_user", id=self.user_1.id),
            headers=self.get_auth_headers(self.user_1_login_data),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'code': 200,
            'type': 'OK',
        })
        self.assertFalse(
            Session().query(user_table).filter_by(id=self.user_1.id).one_or_none()
        )

    def test_delete_another_user(self):
        resp = self.client.delete(
            url_for("api.delete_user", id=self.user_2.id),
            headers=self.get_auth_headers(self.user_1_login_data),
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'UNAUTHORIZED_ACCESS',
        })
        self.assertTrue(
            Session().query(user_table).filter_by(id=self.user_2.id).one_or_none()
        )


class TestGetInventory(BaseTC):
    def setUp(self):
        super().setUp()
        self.user_1 = dbu.create_entry(user_table, **self.user_1_data_pass)
        dbu.create_entry(car_table, **{
            **self.car_1_data})
        dbu.create_entry(car_table, **{
            **self.car_2_data})

    def test_get_inventory(self):
        resp = self.client.get(
            url_for("api.get_inventory"),
            headers=self.get_auth_headers(self.user_1_login_data),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, [
            {
                'carId': ANY,
                'name': self.car_1_data['name'],
                'price': self.car_1_data['price'],
            },
            {
                'carId': ANY,
                'name': self.car_2_data['name'],
                'price': self.car_2_data['price'],
            }
        ])

    def test_unauthorized(self):
        resp = self.client.get(url_for("api.get_inventory"))

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'msg': 'Missing Authorization Header'
        })


class TestGetCarById(BaseTC):
    def setUp(self):
        super().setUp()
        dbu.create_entry(user_table, **self.user_1_data_pass)
        self.car_1 = dbu.create_entry(car_table, **self.car_1_data)

    def test_get_car_by_id(self):
        resp = self.client.get(
            url_for("api.get_car_by_id", carId=self.car_1.carId),
            headers=self.get_auth_headers(self.user_1_login_data),
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'carId': self.car_1.carId,
            'name': self.car_1_data['name'],
            'price': self.car_1_data['price']
        })

    def test_unauthorized(self):
        resp = self.client.get(url_for("api.get_car_by_id", carId=self.car_1.carId))

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'msg': 'Missing Authorization Header'
        })


class TestCreateCar(BaseTC):
    def setUp(self):
        super().setUp()
        dbu.create_entry(user_table, **self.admin_data_pass)
        dbu.create_entry(user_table, **self.user_1_data_pass)

    def test_create_car(self):
        resp = self.client.post(
            url_for("api.create_car"),
            json={"name": self.car_1_data["name"], "price": self.car_1_data["price"]},
            headers=self.get_auth_headers(self.admin_login_data),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'carId': ANY
        })
        self.assertTrue(
            Session().query(car_table).filter_by(name=self.car_1_data['name']).first()
        )

    def test_not_admin(self):
        resp = self.client.post(
            url_for("api.create_car"),
            json={"name": self.car_1_data["name"], "price": self.car_1_data["price"]},
            headers=self.get_auth_headers(self.user_1_login_data),
        )
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'UNAUTHORIZED_ACCESS',
        })
        self.assertFalse(
            Session().query(car_table).filter_by(name=self.car_1_data['name']).one_or_none()
        )

    def test_unauthorized(self):
        resp = self.client.post(
            url_for("api.create_car"),
            json={"name": self.car_1_data["name"], "price": self.car_1_data["price"]},
        )
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'msg': 'Missing Authorization Header'
        })
        self.assertFalse(
            Session().query(car_table).filter_by(name=self.car_1_data['name']).one_or_none()
        )


class TestUpdateCar(BaseTC):
    def setUp(self):
        super().setUp()
        self.car_1 = dbu.create_entry(car_table, **self.car_1_data)
        dbu.create_entry(user_table, **self.admin_data_pass)
        dbu.create_entry(user_table, **self.user_1_data_pass)

    def test_update_car(self):
        resp = self.client.put(
            url_for("api.update_car", carId=self.car_1.carId),
            json={
                **self.car_1_data,
                "price": 1500.0
            },
            headers=self.get_auth_headers(self.admin_login_data),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'code': 200,
            'type': 'OK',
        })
        self.assertTrue(
            Session().query(car_table).filter_by(price=1500.0).first()
        )

    def test_not_admin(self):
        resp = self.client.put(
            url_for("api.update_car", carId=self.car_1.carId),
            json={
                **self.car_1_data,
                "price": 1500.0
            },
            headers=self.get_auth_headers(self.user_1_login_data),
        )
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'UNAUTHORIZED_ACCESS',
        })
        self.assertFalse(
            Session().query(car_table).filter_by(price=1500.0).one_or_none()
        )

    def test_unauthorized(self):
        resp = self.client.put(
            url_for("api.update_car", carId=self.car_1.carId),
            json={
                **self.car_1_data,
                "price": 1500.0
            },
        )
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'msg': 'Missing Authorization Header'
        })
        self.assertFalse(
            Session().query(car_table).filter_by(price=1500.0).one_or_none()
        )


class TestDeleteCar(BaseTC):
    def setUp(self):
        super().setUp()
        self.car_1 = dbu.create_entry(car_table, **self.car_1_data)
        dbu.create_entry(user_table, **self.admin_data_pass)
        dbu.create_entry(user_table, **self.user_1_data_pass)

    def test_delete_car(self):
        resp = self.client.delete(
            url_for("api.delete_car", carId=self.car_1.carId),
            headers=self.get_auth_headers(self.admin_login_data),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'code': 200,
            'type': 'OK',
        })
        self.assertFalse(
            Session().query(car_table).filter_by(carId=self.car_1.carId).one_or_none()
        )

    def test_not_admin(self):
        resp = self.client.delete(
            url_for("api.delete_car", carId=self.car_1.carId),
            headers=self.get_auth_headers(self.user_1_login_data),
        )
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'UNAUTHORIZED_ACCESS',
        })
        self.assertTrue(
            Session().query(car_table).filter_by(carId=self.car_1.carId).one_or_none()
        )

    def test_unauthorized(self):
        resp = self.client.delete(url_for("api.delete_car", carId=self.car_1.carId))

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'msg': 'Missing Authorization Header'
        })
        self.assertTrue(
            Session().query(car_table).filter_by(carId=self.car_1.carId).one_or_none()
        )


class TestPlaceOrder(BaseTC):
    def setUp(self):
        super().setUp()
        self.car_1 = dbu.create_entry(car_table, **self.car_1_data)
        self.user = dbu.create_entry(user_table, **self.user_1_login_data)

    def test_place_order(self):

        resp = self.client.post(
            url_for("api.place_order", carId=self.car_1.carId),
            json={"shipDate": self.order_1_data["shipDate"], "returnDate": self.order_1_data["returnDate"]},
            headers=self.get_auth_headers(self.user_1_login_data),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'id': ANY
        })
        self.assertTrue(
            Session().query(order_table).filter_by(shipDate=self.order_1_data['shipDate'],
                                                   returnDate=self.order_1_data['returnDate']).one()
        )

    def test_unauthorized(self):
        resp = self.client.post(
            url_for("api.place_order", carId=self.car_1.carId),
            json={"shipDate": self.order_1_data["shipDate"], "returnDate": self.order_1_data["returnDate"]},
        )
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'msg': 'Missing Authorization Header'
        })
        self.assertFalse(
            Session().query(order_table).filter_by(shipDate=self.order_1_data['shipDate'],
                                                   returnDate=self.order_1_data['returnDate']).one_or_none()
        )


class TestGetOrders(BaseTC):
    def setUp(self):
        super().setUp()
        dbu.create_entry(user_table, **self.admin_data_pass)
        self.user = dbu.create_entry(user_table, **self.user_1_data_pass)
        self.car_1 = dbu.create_entry(car_table, **self.car_1_data)
        self.car_2 = dbu.create_entry(car_table, **self.car_2_data)
        dbu.create_entry(order_table, **self.order_1_data, carId=self.car_1.carId, userId=self.user.id)
        dbu.create_entry(order_table, **self.order_2_data, carId=self.car_2.carId, userId=self.user.id)

    def test_get_orders(self):
        resp = self.client.get(
            url_for("api.get_orders"),
            headers=self.get_auth_headers(self.admin_login_data),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, [
            {
                'id': ANY,
                'carId': self.car_1.carId,
                'complete': self.order_1_data['complete'],
                'returnDate': self.order_1_data['returnDate'],
                'shipDate': self.order_1_data['shipDate'],
                'status': self.order_1_data['status'],
                'userId': self.user.id
            },
            {
                'id': ANY,
                'carId': self.car_2.carId,
                'complete': self.order_2_data['complete'],
                'returnDate': self.order_2_data['returnDate'],
                'shipDate': self.order_2_data['shipDate'],
                'status': self.order_2_data['status'],
                'userId': self.user.id
            }
        ])

    def test_unauthorized(self):
        resp = self.client.get(url_for("api.get_orders"))
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'msg': 'Missing Authorization Header',
        })

    def test_not_admin(self):
        resp = self.client.get(
            url_for("api.get_orders"),
            headers=self.get_auth_headers(self.user_1_login_data),
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'UNAUTHORIZED_ACCESS',
        })


class TestGetOrder(BaseTC):
    def setUp(self):
        super().setUp()
        self.car_1 = dbu.create_entry(car_table, **self.car_1_data)
        self.user = dbu.create_entry(user_table, **self.user_1_data_pass)
        self.order_1 = dbu.create_entry(order_table, **self.order_1_data, carId=self.car_1.carId,
                                        userId=self.user.id)

    def test_get_order_by_id(self):
        resp = self.client.get(
            url_for("api.get_order_by_id", carId=self.order_1.carId, orderId=self.order_1.id),
            headers=self.get_auth_headers(self.user_1_login_data),
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'id': ANY,
            'carId': self.order_1.carId,
            'complete': self.order_1_data['complete'],
            'returnDate': self.order_1_data['returnDate'],
            'shipDate': self.order_1_data['shipDate'],
            'status': self.order_1_data['status'],
            'userId': self.user.id
        })

    def test_unauthorized(self):
        resp = self.client.get(url_for("api.get_order_by_id", carId=self.order_1.carId,
                                       orderId=self.order_1.id))

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'msg': 'Missing Authorization Header'
        })


class TestDeleteOrder(BaseTC):
    def setUp(self):
        super().setUp()
        self.car_1 = dbu.create_entry(car_table, **self.car_1_data)
        self.user = dbu.create_entry(user_table, **self.user_1_data_pass)
        self.order_1 = dbu.create_entry(order_table, **self.order_1_data, carId=self.car_1.carId,
                                        userId=self.user.id)

    def test_delete_order(self):
        resp = self.client.delete(
            url_for("api.delete_order", carId=self.order_1.carId, orderId=self.order_1.id),
            headers=self.get_auth_headers(self.user_1_login_data),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'code': 200,
            'type': 'OK',
        })
        self.assertFalse(
            Session().query(order_table).filter_by(shipDate=self.order_1_data['shipDate'],
                                                   returnDate=self.order_1_data['returnDate']).one_or_none()
        )

    def test_unauthorized(self):
        resp = self.client.delete(url_for("api.delete_order", carId=self.order_1.carId, orderId=self.order_1.id))

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'msg': 'Missing Authorization Header'
        })
        self.assertTrue(
            Session().query(order_table).filter_by(shipDate=self.order_1_data['shipDate'],
                                                   returnDate=self.order_1_data['returnDate']).one_or_none()
        )


if __name__ == '__main__':
    unittest.main()
