from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class FaceStorage(S3Boto3Storage):
    location = settings.AWS_FACE_LOCATION
    file_overwrite = False


class EventStorage(S3Boto3Storage):
    location = settings.AWS_EVENT_LOCATION
    file_overwrite = False
