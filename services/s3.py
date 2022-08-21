import boto3
from botocore.exceptions import ClientError

from decouple import config
from werkzeug.exceptions import InternalServerError


class S3Service:
    """
    A class which represents integration with third party services - Amazon S3 buckets.
    Stores the data in a cloud and prevents overloading of the server memory.
    """
    def __init__(self):
        self.key = config("AWS_ACCESS_KEY")
        self.secret = config("AWS_SECRET_KEY")
        self.s3 = boto3.client("s3", aws_access_key_id=self.key, aws_secret_access_key=self.secret)
        self.bucket = config("AWS_BUCKET")

    def upload_cert(self, path, key, ext):
        try:
            self.s3.upload_file(path, self.bucket, key, ExtraArgs={'ACL': 'public-read', 'ContentType': f'image/{ext}'})
            return f"https://{config('AWS_BUCKET')}.s3.{config('AWS_REGION')}.amazonaws.com/{key}"
        except ClientError:
            raise InternalServerError("S3 is currently not available")
