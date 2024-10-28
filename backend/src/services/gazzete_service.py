import os

import requests
from bs4 import BeautifulSoup


def list_gazettes(year):
    # Example usage
    url = f"https://new.kenyalaw.org/gazettes/{year}"  # Replace with your target URL

    def get_links_and_text():
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Use CSS selector to find all matching elements
            elements = soup.select('#doc-table')

            # Extract links and text from the matching elements
            results = []
            for element in elements:
                rows = element.find_all('tr')
                for row in rows:
                    cells = row.find_all('td', class_='cell-title')
                    if cells:
                        # print(len(cells))
                        # pprint(cells[0])
                        link = cells[0].find('a')['href']
                        title = cells[0].text.strip()
                        results.append((title, link))
            return results
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None

    links_and_text = get_links_and_text()

    return links_and_text

def download_gazette(link,title, destination_folder):
    file_path = os.path.join(destination_folder, f"{title}.pdf")
    if os.path.exists(file_path):
        print(f"\t Skipped {title} . Already exists.")
        return file_path
    os.makedirs(destination_folder, exist_ok=True)
    url = f"https://new.kenyalaw.org{link}/source.pdf"
    # print(link)
    # print(url)

    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"\t Downloaded {title} to {file_path}")
        return file_path
    else:
        print(f"\t Failed to download {title}. Status code: {response.status_code}")
