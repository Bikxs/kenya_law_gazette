import unittest
import requests

URL = "https://icfb7s3gub.execute-api.us-east-1.amazonaws.com/Stage"


class GazetteTestsIT(unittest.TestCase):
    def download_year(self, year):
        response = requests.post(f"{URL}/readgazettes", json={"year": year})
        self.assertEqual(response.status_code, 200)
        # print(response.text)

    def test_download_2020(self):
        self.download_year(2020)

    def test_download_2021(self):
        self.download_year(2021)

    def test_download_2022(self):
        self.download_year(2022)

    def test_download_2023(self):
        self.download_year(2023)

    def test_download_2024(self):
        self.download_year(2024)


if __name__ == '__main__':
    unittest.main()
