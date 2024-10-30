import unittest
import requests

URL = "https://5kpv5e08h4.execute-api.eu-central-1.amazonaws.com/Stage"


class GazetteTestsIT(unittest.TestCase):
    def download_year(self, year):
        response = requests.post(f"{URL}/readgazettes", json={"year": year})
        # self.assertEqual(response.status_code, 200)
        print(f"{year}:{response.text}")

    def test_download_all(self):
        years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
        for year in years:
            self.download_year(year)


if __name__ == '__main__':
    unittest.main()
