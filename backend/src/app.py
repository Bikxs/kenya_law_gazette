from gazzete_service import queue_gazettes_download, download_gazette as download_gazette_service 
import json

def queue_gazettes_downloads(event, context):
    # print(event)
    year = json.loads(event['body'])['year']
    if not year:
        return {'statusCode': 400, 'body': 'Year is required'}
    print(f"Downloading year: {year}")
    try:
        queue_gazettes_download(year)
    except Exception as e:
        return {'statusCode': 500, 'body': f'Unexpected error: {str(e)}'}
    return {'statusCode': 200, 'body': 'Gazettes download queued successfully'}


def download_gazette(event, context):
    
    # print(event)
    payload = json.loads(event['Records'][0]['body'])
    year = payload['year']
    link = payload['link']
    title = payload['title']
    if not year:
        return {'statusCode': 400, 'body': 'Year is required'}
    if not link:
        return {'statusCode': 400, 'body': 'Link is required'}
    if not title:
        return {'statusCode': 400, 'body': 'Title is required'}
    print(f"Downloading gazette {title} for {year}")
    try:
        download_gazette_service(link=link,year=year, title=title)
    except Exception as e:
        print(f"Error downloading {title}: {e}")
        return {'statusCode': 500, 'body': f'Unexpected error: {str(e)}'}
    return {'statusCode': 200, 'body': 'Gazette downloaded successfully'}
