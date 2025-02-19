import boto3
import random
from whizzo_project.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_KEY, AWS_BUCKET_NAME
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import string

access_key_id = AWS_ACCESS_KEY_ID
secret_access_key = AWS_SECRET_KEY
bucket_name = AWS_BUCKET_NAME

def save_image(image):
    image_name = "".join((image.name).split(" ")).replace("%", "")
    for i in image_name:
        if i not in string.ascii_letters + string.digits + string.punctuation:
            image_name = "file"
            break
    image_name = "{}_{}".format(random.randint(100000, 999999), image_name)
    s3 = boto3.client("s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    acl="public-read"
    url = s3.upload_fileobj(
            image,
            bucket_name,
            image_name,
            ExtraArgs={
                "ACL": acl,
                "ContentType": image.content_type
            }
        )
    s3_location = "https://{}.s3.ap-south-1.amazonaws.com/".format(bucket_name)
    return "{}{}".format(s3_location, image_name), image_name


def save_file_conversion(file, image_name, content_type):
    if '.' in image_name:
        name, extension = image_name.rsplit('.', 1)
    else:
        name = image_name
        extension = "jpg"  
    if not name or any(i not in string.ascii_letters + string.digits for i in name):
        image_name = f"file.{extension}"
    s3 = boto3.client("s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    acl = "public-read"
    url = s3.upload_file(
            file,
            bucket_name,
            image_name,
            ExtraArgs={
                "ACL": acl,
                "ContentType": content_type
            }
        )
    s3_location = "https://{}.s3.ap-south-1.amazonaws.com/".format(bucket_name)
    
    return "{}{}".format(s3_location, image_name), image_name


def save_file_conversion_for_csv(file, filename, content_type):
    s3 = boto3.client("s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    acl = "public-read"
    s3.upload_fileobj(
        file,
        bucket_name,
        filename,
        ExtraArgs={
            "ACL": acl,
            "ContentType": content_type
        }
    )
    s3_location = f"https://{bucket_name}.s3.amazonaws.com/"
    return f"{s3_location}{filename}", filename

def save_file_conversion_csv(file_content, filename, content_type):
    file_like_object = ContentFile(file_content)    
    media_url, saved_filename = save_file_conversion_for_csv(file_like_object, filename, content_type)
    return media_url, saved_filename

def saveFile(image_path, file_type):
    image_name = f"{random.randint(1000, 9999)}_{image_path}"
    s3 = boto3.client("s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    acl="public-read"
    with open(image_path, 'rb') as image:
        url = s3.upload_fileobj(
                image,
                bucket_name,
                image_name,
                ExtraArgs={
                    "ACL": acl,
                    "ContentType": file_type
                }
            )
        s3_location = "https://{}.s3.ap-south-1.amazonaws.com/".format(bucket_name)
        return "{}{}".format(s3_location, image_name), image_name