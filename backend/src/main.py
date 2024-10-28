import os.path
import random

from backend.src.services.gazzete_service import list_gazettes, download_gazette

years = [2020, 2021, 2022, 2023, 2024]
if __name__ == '__main__':
    for year in years:
        print("-" * 80)
        print(f"Year {year}")
        gazettes = random.sample(list_gazettes(year), k=3)
        for title, link in gazettes:
            download_gazette(link, title=title, destination_folder=os.path.join(f"data", f"{year}"))