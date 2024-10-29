import os
from gazzete_service import download_gazettes

def download(event, context):
    # print(event)
    year = event['year']
    if not year:
        return {'statusCode': 400, 'body': 'Year is required'}
    try:
        download_gazettes(year)
    except Exception as e:
        return {'statusCode': 500, 'body': f'Unexpected error: {str(e)}'}
