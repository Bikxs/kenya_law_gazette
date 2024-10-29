import os

import boto3
import requests
from botocore.exceptions import ClientError
from bs4 import BeautifulSoup

# Initialize S3 client
s3_client = boto3.client('s3')

# S3 bucket name
S3_BUCKET_NAME = 'XXXXXXXXXXXXXXXXXXX'  # Replace with your actual S3 bucket name


def _list_gazettes(year):
    url = f"https://new.kenyalaw.org/gazettes/{year}"

    def get_links_and_text():
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            elements = soup.select('#doc-table')
            results = []
            for element in elements:
                rows = element.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if cells:
                        link = cells[0].find('a')['href']
                        title = cells[0].text.strip()
                        results.append((title, link))
            return results
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None

    return get_links_and_text()


def download_gazettes(year):
    gazettes = _list_gazettes(year)
    for title, link in gazettes:
        download_gazette(link, title=title, destination_folder=os.path.join(f"data", f"{year}"))


def download_gazette(link, title, year):
    s3_key = f"{year}/{title}.pdf"

    # Check if the file already exists in S3
    try:
        s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
        print(f"\t Skipped {title}. Already exists in S3.")
        return s3_key
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            # The file doesn't exist in S3, proceed with download
            pass
        else:
            # Something else has gone wrong
            print(f"\t Error checking S3 for {title}: {str(e)}")
            return None

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


