import json
from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from db import db
from models import SuggestionModel
from services.s3 import S3Service
from services.ses import SESService
from tests.factories import (
    SuggesterFactory,
    AdminFactory,
    SuggestionFactory,
    SuggesterUploadFactory,
)
from tests.helpers import generate_token, encoded_certificate


class TestSuggestion(TestCase):
    url = "/suggesters/suggestions/"

    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_suggestion_missing_input_fields_raises(self):
        sugg = SuggesterFactory()
        token = generate_token(sugg)

        suggestions = SuggestionModel.query.all()
        self.assertEqual(len(suggestions), 0)

        data = {
            "title": "TestTitle",
            "content": "We have a wonderful tests here.",
            "assessment_rate": 1,
            "certificate": encoded_certificate,
            "certificate_extension": "jpeg",
        }
        for key in data:
            current_data = data.copy()
            current_data.pop(key)
            resp = self.client.post(
                self.url,
                data=json.dumps(current_data),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                },
            )
            message = resp.json["message"]
            expected_message = (
                "Invalid fields {'" + key + "': ['Missing data for required field.']}"
            )
            self.assert400(resp)
            self.assertEqual(message, expected_message)

        suggestions = SuggestionModel.query.all()
        self.assertEqual(len(suggestions), 0)

    @patch.object(S3Service, "upload_cert", return_value="some.s3.url")
    def test_create_suggestion(self, mocked_s3):
        sugg = SuggesterFactory()
        token = generate_token(sugg)

        suggestions = SuggestionModel.query.all()
        self.assertEqual(len(suggestions), 0)

        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "title": "TestTitle",
            "content": "We have a wonderful tests here.",
            "assessment_rate": 1,
            "certificate": encoded_certificate,
            "certificate_extension": "jpeg",
        }
        resp = self.client.post(self.url, headers=headers, json=data)
        expected_resp = {
            "id": 1,
            "status": "Waiting for an overview",
            "course_certificate_url": "some.s3.url",
            "title": "TestTitle",
            "content": "We have a wonderful tests here.",
            "assessment_rate": 1,
        }
        assert resp.status_code == 201
        resp = resp.json
        resp.pop("created_on")
        self.assertEqual(resp, expected_resp)

        suggestions = SuggestionModel.query.all()
        self.assertEqual(len(suggestions), 1)

    @patch.object(SESService, "send_mail", return_value=None)
    def test_upload_suggestion(self, mocked_ses):
        suggester = SuggesterUploadFactory()
        suggestion = SuggestionFactory()
        admin = AdminFactory()
        upload_url = f"/admins/suggestions/{suggestion.id}/upload/"
        token = generate_token(admin)
        headers = {"Authorization": f"Bearer {token}"}

        suggestions = SuggestionModel.query.all()
        self.assertEqual(len(suggestions), 1)

        resp = self.client.put(upload_url, headers=headers)
        assert resp.status_code == 200

        result = SuggestionModel.query.filter_by(status="accepted").all()
        self.assertEqual(len(result), 1)

    @patch.object(SESService, "send_mail", return_value=None)
    def test_reject_suggestion(self, mocked_ses):
        suggester = SuggesterUploadFactory()
        suggestion = SuggestionFactory()
        admin = AdminFactory()
        upload_url = f"/admins/suggestions/{suggestion.id}/reject/"
        token = generate_token(admin)
        headers = {"Authorization": f"Bearer {token}"}

        suggestions = SuggestionModel.query.all()
        self.assertEqual(len(suggestions), 1)

        resp = self.client.put(upload_url, headers=headers)
        assert resp.status_code == 200

        result = SuggestionModel.query.filter_by(status="rejected").all()
        self.assertEqual(len(result), 1)
