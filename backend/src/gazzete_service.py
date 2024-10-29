import json
import os

import boto3
import requests
from botocore.exceptions import ClientError
from bs4 import BeautifulSoup

# Initialize S3 client
s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')

# S3 bucket name
S3_BUCKET_NAME = os.environ.get('GAZETTESBUCKET_BUCKET_NAME')
QUEUE_URL = os.environ.get('PENDINGGAZETTESDOWNLOADQUEUE_QUEUE_URL')
QUEUE_ARN = os.environ.get('PENDINGGAZETTESDOWNLOADQUEUE_QUEUE_ARN')


def list_gazettes(year):
    url = f"https://new.kenyalaw.org/gazettes/{year}"
    print(f"Hitting URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Response status 200. Legnth = {len(response.content)}")
        soup = BeautifulSoup(response.content, 'html.parser')
        elements = soup.select('#doc-table')
        results = []
        for element in elements:
            rows = element.find_all('tr')
            for row in rows:
                cells = row.find_all('td', class_='cell-title')
                if cells:
                    link = cells[0].find('a')['href']
                    title = cells[0].text.strip()
                    results.append((title, link))
        return results
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []


def gazette_is_downloaded(year, title, print_output=False):
    s3_key = f"{year}/{title}.pdf"
    try:
        s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
        if print_output:
            print(f"\t Skipped {title}. Already exists in S3.")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            pass
        else:
            if print_output:
                print(f"\t Error checking S3 for {title}: {str(e)}")
        return False


def queue_gazettes_download(year):
    gazettes = list_gazettes(year)
    for title, link in gazettes:
        if gazette_is_downloaded(year, title, print_output=True):
            continue
        message = dict(link=link, year=year, title=title)
        try:
            # Send the message to the SQS queue
            response = sqs_client.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=json.dumps(message)
            )
            print(f"Queued gazette {title}/{year} for download. Message ID: {response['MessageId']}")
        except Exception as e:
            print(f"Error queueing gazette download: {str(e)}")


def download_gazette(link, year, title):
    s3_key = f"{year}/{title}.pdf"

    # Check if the file already exists in S3
    if gazette_is_downloaded(year, title, print_output=True) == True:
        return s3_key

    url = f"https://new.kenyalaw.org{link}/source.pdf"

    response = requests.get(url)
    if response.status_code == 200:
        try:
            s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=s3_key, Body=response.content)
            print(f"\t Downloaded {title} to S3://{S3_BUCKET_NAME}/{s3_key}")
            return s3_key
        except ClientError as e:
            print(f"\t Failed to upload {title} to S3: {str(e)}")
    else:
        print(f"\t Failed to download {title}. Status code: {response.status_code}")
