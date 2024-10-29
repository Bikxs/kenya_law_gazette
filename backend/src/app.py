from gazzete_service import queue_gazettes_download, download_gazette


def queue_gazettes_downloads(event, context):
    year = event['year']
    if not year:
        return {'statusCode': 400, 'body': 'Year is required'}
    print(f"Downloading year: {year}")
    try:
        queue_gazettes_download(year)
    except Exception as e:
        return {'statusCode': 500, 'body': f'Unexpected error: {str(e)}'}
    return {'statusCode': 200, 'body': 'Gazettes download queued successfully'}


def download_gazette(event, context):
    year = event['year']
    link = event['link']
    title = event['title']
    if not year:
        return {'statusCode': 400, 'body': 'Year is required'}
    if not link:
        return {'statusCode': 400, 'body': 'Link is required'}
    if not title:
        return {'statusCode': 400, 'body': 'Title is required'}
    print(f"Downloading gazette {title} for {year}")
    try:
        download_gazette(link, year, title)
    except Exception as e:
        return {'statusCode': 500, 'body': f'Unexpected error: {str(e)}'}
    return {'statusCode': 200, 'body': 'Gazette downloaded successfully'}
