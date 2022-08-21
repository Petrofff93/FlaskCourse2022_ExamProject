import boto3
from decouple import config


class SESService:
    def __init__(self):
        self.ses = boto3.client(
            "ses",
            region_name=config("AWS_REGION"),
            aws_access_key_id=config("AWS_ACCESS_KEY"),
            aws_secret_access_key=config("AWS_SECRET_KEY"),
        )

    def send_mail(self, subject, recipients, data_text):
        body = {}
        body.update({"Text": {"Data": data_text, "Charset": "UTF-8"}})

        try:
            self.ses.send_email(
                Source=config("AWS_SOURCE_MAIL"),
                Destination={
                    "ToAddresses": recipients,
                    "CcAddresses": [],
                    "BccAddresses": [],
                },
                Message={
                    "Subject": {"Data": subject, "Charset": "UTF-8"},
                    "Body": body,
                },
            )
        except Exception as err:
            raise err
