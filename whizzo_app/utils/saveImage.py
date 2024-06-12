import boto3
import random
from whizzo_project.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_KEY, AWS_BUCKET_NAME

access_key_id = AWS_ACCESS_KEY_ID
secret_access_key = AWS_SECRET_KEY
bucket_name = AWS_BUCKET_NAME

def save_image(image):
    image_name = "".join((image.name).split(" "))
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
    # image_name = f"{random.randint(10000, 99999)}_{image_name}"
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