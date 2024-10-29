import os

import boto3
from botocore.exceptions import ClientError

from gazzete_service import download_gazettes

s3 = boto3.client('s3')
bucket_name = os.environ['S3_KENYA_GAZETTE_BUCKET_NAME', 'KENYA_GAZETTES']


def download(event, context):
    print(event)
    year = event.get('year')
    if not year:
        return {'statusCode': 400, 'body': 'Year is required'}
    try:
        download_gazettes(year)
    except ClientError as e:
        return {'statusCode': 500, 'body': f'Error: {str(e)}'}
    except Exception as e:
        return {'statusCode': 500, 'body': f'Unexpected error: {str(e)}'}
