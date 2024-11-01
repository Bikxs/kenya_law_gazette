import unittest
from pprint import pprint

import requests

URL = "https://5kpv5e08h4.execute-api.eu-central-1.amazonaws.com/Stage"


class GazetteTestsIT(unittest.TestCase):
    def download_year(self, year):
        response = requests.post(f"{URL}/readgazettes", json={"year": year})
        # self.assertEqual(response.status_code, 200)
        print(f"{year}:{response.text}")

    def test_download_all(self):
        years = [x for x in range(2010, 2025)]
        pprint(years)
        for year in years:
            self.download_year(year)


if __name__ == '__main__':
    unittest.main()
