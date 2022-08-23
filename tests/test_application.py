import json

from flask_testing import TestCase

from config import create_app
from db import db
from tests.factories import SuggesterFactory
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
            ("DELETE", "/admins/suggestions/rejected/delete/")
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
            ("DELETE", "/admins/suggestions/rejected/delete/")
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
            ("PUT", "/admins/suggestions/1/reject/")
        ]
        user = SuggesterFactory()
        token = generate_token(user)
        headers = {"Authorization": f"Bearer {token}"}
        resp = None

        for method, url in data:
            if method == "PUT":
                resp = self.client.put(url, headers=headers)
            self.assert403(resp)
            self.assertEqual(resp.json, {"message": "Permission denied!"})
