from bucket import bucket as bucket_obj
from celery import shared_task


def all_bucket_object_task():
    result = bucket_obj.get_objects()
    return result


@shared_task
def delete_bucket_object_task(key):
    bucket_obj.delete_object(key)


@shared_task
def download_bucket_object_task(key):
    bucket_obj.download_object(key)
