import boto3
from pathlib import Path
from app.config import *

s3_resource = boto3.client('s3', region_name='eu-west-3')
class Body_Loader:
    def __init__(self, message):
        self.body_key = Path(message[field_names.body_key])
        self.bucket, self.file_path = self.parse_file_url(self.body_key)

    def load_article_body(self) -> str:
        """
        loads document body from s3 bucket
        """
        self.s3_resource = s3_resource
        obj = self.s3_resource.get_object(Bucket=self.bucket, Key=self.file_path)
        return obj['Body'].read().decode("utf8")

    @staticmethod
    def parse_file_url(key: Path) -> tuple:
        """Split the bucket and path part from an S3 file url.

        The url must have one of the forms :
        - https://s3.eu-west-3.amazonaws.com/article.archive.bucket/BERREP/2010/10/BERREP0110201010713043.json
        - s3:article.archive.bucket/BERREP/2010/10/BERREP0110201010713043.json

        :param key: a ``pathlib.Path`` path pointing to an S3 url
        :type key: Path

        :return: a tuple (bucket, path)
        :rtype: tuple
        """
        root = key.parts[0]
        if root == 'https:':
            bucket_index = 2
        elif root == 's3:':
            bucket_index = 1

        bucket = key.parts[bucket_index]
        path = '/'.join(key.parts[bucket_index + 1::])
        return bucket, path
