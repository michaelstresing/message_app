from flask import Flask, jsonify, render_template
from flask import request, Blueprint
import sqlalchemy
from application import models, db
from application.models import Message, Chat
from flask_login import current_user
import os

import logging
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import requests

FileAPI = Blueprint("file_api", __name__)

S3_BUCKET                 = os.environ.get("S3_BUCKET_NAME")
S3_KEY                    = os.environ.get("S3_ACCESS_KEY")
S3_SECRET                 = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION               = f'http://{S3_BUCKET}.s3.amazonaws.com/'

s3_client = boto3.client('s3',
                        aws_access_key_id=S3_KEY,
                        aws_secret_access_key=S3_SECRET,
                        config=Config(signature_version='s3v4'),
                        region_name='us-east-2'
                        )

@FileAPI.route('/upload/', methods=["PUT"])
def upload_test(file_name='/Users/michaelstresing/Desktop/s3test.txt'):

    object_name = "s3test.txt"

    # Generate a presigned S3 POST URL
    response = create_presigned_post(object_name)
    if response is None:
        exit(1)

    http_response = requests.post(response['url'],
                                  data=response['fields'],
                                  files={'file': (object_name, open(file_name, 'rb'))}
                                )

    print(response['url'], response['fields'])
    
    # If successful, returns HTTP status code 204
    logging.info(f'File upload HTTP status code: {http_response.status_code}')

    return f"{http_response.text}"

def create_presigned_post(object_name,
                          fields=None, conditions=None, expiration=3600):

    try:
        response = s3_client.generate_presigned_post('quackio',
                                                        object_name,
                                                        Fields = fields,
                                                        Conditions = conditions,
                                                        ExpiresIn = 3600
                                                    )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


# @FileAPI.route('/retrieve/')
# def get_test(file_name='/Users/michaelstresing/Desktop/s3test.txt')

