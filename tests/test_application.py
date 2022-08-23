from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from config import create_app
from db import db
from models import SuggesterModel
from tests.factories import (
    SuggesterFactory,
    SuggesterEmailFactory,
    SuggesterPhoneFactory,
    SuggesterFactoryLoginUser,
)
from tests.helpers import generate_token


class TestApp(TestCase):
    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_missing_token_raises(self):
        for method, url in [
            ("PUT", "/admins/suggestions/1/upload/"),
            ("PUT", "/admins/suggestions/1/reject/"),
            ("GET", "/suggesters/suggestions/"),
            ("POST", "/suggesters/suggestions/"),
            ("DELETE", "/admins/suggestions/rejected/delete/"),
        ]:

            resp = None

            if method == "POST":
                resp = self.client.post(url)
            elif method == "GET":
                resp = self.client.get(url)
            elif method == "PUT":
                resp = self.client.put(url)
            elif method == "DELETE":
                resp = self.client.delete(url)

            self.assert401(resp)
            self.assertEqual(resp.json, {"message": "Token is missing!"})

    def test_invalid_token_raises(self):
        headers = {"Authorization": "Bearer well231"}

        for method, url in [
            ("PUT", "/admins/suggestions/1/upload/"),
            ("PUT", "/admins/suggestions/1/reject/"),
            ("GET", "/suggesters/suggestions/"),
            ("POST", "/suggesters/suggestions/"),
            ("DELETE", "/admins/suggestions/rejected/delete/"),
        ]:

            resp = None

            if method == "POST":
                resp = self.client.post(url, headers=headers)
            elif method == "GET":
                resp = self.client.get(url, headers=headers)
            elif method == "PUT":
                resp = self.client.put(url, headers=headers)
            elif method == "DELETE":
                resp = self.client.delete(url, headers=headers)

            self.assert401(resp)
            self.assertEqual(resp.json, {"message": "Token is invalid!"})

    def test_suggester_have_no_permission_raises(self):
        data = [
            ("PUT", "/admins/suggestions/1/upload/"),
            ("PUT", "/admins/suggestions/1/reject/"),
            ("DELETE", "/admins/suggestions/rejected/delete/"),
        ]
        user = SuggesterFactory()
        token = generate_token(user)
        headers = {"Authorization": f"Bearer {token}"}
        resp = None

        for method, url in data:
            if method == "PUT":
                resp = self.client.put(url, headers=headers)
            elif method == "DELETE":
                resp = self.client.delete(url, headers=headers)

            self.assert403(resp)
            self.assertEqual(resp.json, {"message": "Permission denied!"})

    def test_register_schema_raises_invalid_first_name(self):
        url = "/register/"
        headers = {"Content-Type": "application/json"}
        data = {
            "last_name": "Testov",
            "email": "test@test.com",
            "password": "Password123!@",
            "phone_number": "+359876765123",
        }

        # Missing first_name
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        expected = {
            "message": "Invalid fields {'first_name': ['Missing data for required field.']}"
        }
        actual = resp.json
        self.assertEqual(expected, actual)

        # Too short first_name
        data["first_name"] = "T"
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        expected = {
            "message": "Invalid fields {'first_name': ['Length must be between 2 and 30.']}"
        }

        actual = resp.json
        self.assertEqual(expected, actual)

        # Too long first_name
        data["first_name"] = "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        expected = {
            "message": "Invalid fields {'first_name': ['Length must be between 2 and 30.']}"
        }
        actual = resp.json
        self.assertEqual(expected, actual)

    def test_register_schema_raises_invalid_last_name(self):
        url = "/register/"
        headers = {"Content-Type": "application/json"}
        data = {
            "first_name": "Testov",
            "email": "test@test.com",
            "password": "Password123!@",
            "phone_number": "+359876765123",
        }

        # Missing first_name
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        expected = {
            "message": "Invalid fields {'last_name': ['Missing data for required field.']}"
        }
        actual = resp.json
        self.assertEqual(expected, actual)

        # Too short last_name
        data["last_name"] = "T"
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        expected = {
            "message": "Invalid fields {'last_name': ['Length must be between 2 and 30.']}"
        }

        actual = resp.json
        self.assertEqual(expected, actual)

        # Too long last_name
        data["last_name"] = "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        expected = {
            "message": "Invalid fields {'last_name': ['Length must be between 2 and 30.']}"
        }
        actual = resp.json
        self.assertEqual(expected, actual)

        users = SuggesterModel.query.all()
        self.assertEqual(len(users), 0)

    def test_register_schema_raises_invalid_email(self):
        url = "/register/"
        headers = {"Content-Type": "application/json"}
        data = {
            "first_name": "Testov",
            "last_name": "Testovov",
            "password": "Password123!@",
            "phone_number": "+359876765123",
        }

        # Missing email address
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        expected = {
            "message": "Invalid fields {'email': ['Missing data for required field.']}"
        }
        actual = resp.json
        self.assertEqual(expected, actual)

        # Invalid email address
        data["email"] = "t.t@.t"
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        expected = {
            "message": "Invalid fields {'email': ['Not a valid email address.']}"
        }
        actual = resp.json
        self.assertEqual(expected, actual)

        users = SuggesterModel.query.all()
        self.assertEqual(len(users), 0)

    def test_register_schema_raises_email_already_registered(self):
        url = "/register/"
        user = SuggesterEmailFactory()
        token = generate_token(user)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        data = {
            "first_name": "Testov",
            "last_name": "Testovov",
            "email": "test@test.com",
            "password": "Password123!@",
            "phone_number": "+359876765123",
        }
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        expected = {"message": "Invalid fields {'email': ['Email already exists!']}"}
        actual = resp.json
        self.assertEqual(expected, actual)

        users = SuggesterModel.query.all()
        self.assertEqual(len(users), 1)

    def test_register_schema_raises_invalid_phone_number(self):
        url = "/register/"
        headers = {"Content-Type": "application/json"}
        data = {
            "first_name": "Testov",
            "last_name": "Testovov",
            "email": "test@test.com",
            "password": "Password123!@",
        }
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        expected = {
            "message": "Invalid fields {'phone_number': ['Missing data for required field.']}"
        }
        actual = resp.json
        self.assertEqual(expected, actual)

        users = SuggesterModel.query.all()
        self.assertEqual(len(users), 0)

    def test_register_schema_raises_when_phone_number_exists(self):
        url = "/register/"
        user = SuggesterPhoneFactory()
        token = generate_token(user)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        data = {
            "first_name": "Testov",
            "last_name": "Testovov",
            "email": "test@test.com",
            "password": "Password123!@",
            "phone_number": "+359876870777",
        }
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        expected = {
            "message": "Invalid fields {'phone_number': ['User with that phone number already exists!']}"
        }
        actual = resp.json
        self.assertEqual(expected, actual)

        users = SuggesterModel.query.all()
        self.assertEqual(len(users), 1)

    def test_register_successfully_adds_user(self):
        url = "/register/"
        headers = {"Content-Type": "application/json"}

        data = {
            "first_name": "Testov",
            "last_name": "Testovov",
            "email": "test@test.com",
            "password": "Password123!@",
            "phone_number": "+359876870777",
        }
        resp = self.client.post(url, headers=headers, json=data)
        assert resp.status_code == 201
        users = SuggesterModel.query.all()
        self.assertEqual(len(users), 1)

    def test_user_login_raises_when_invalid_credentials(self):
        url = "/login/base_user/"
        headers = {"Content-Type": "application/json"}

        sugg = SuggesterFactoryLoginUser()

        data = {"email": "test@test.com", "password": "231245EP@"}
        # Test with false password
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        expected = {"message": "Credentials are not valid!"}
        actual = resp.json
        self.assertEqual(expected, actual)

        # Test with false email
        data = {"email": "test@testfalse.com", "password": "231245EP@"}
        # Test with false password
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)
        expected = {"message": "There is no such email! Please Signup"}
        actual = resp.json
        self.assertEqual(expected, actual)

    def test_user_login_successfully(self):
        url = "/login/base_user/"
        headers = {"Content-Type": "application/json"}

        user = SuggesterFactory()

        data = {"email": user.email, "password": user.password}
        user.password = generate_password_hash(user.password)
        resp = self.client.post(url, headers=headers, json=data)
        self.assert200(resp)
