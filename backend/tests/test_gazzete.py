import unittest

from backend.src.gazzete_service import list_gazettes


class GazetteTests(unittest.TestCase):

    def test_get_list_2020(self):
        gazettes = list_gazettes(2020)
        self.assertTrue(len(gazettes) >= 1)

    def test_get_list_2021(self):
        gazettes = list_gazettes(2021)
        self.assertTrue(len(gazettes) >= 1)


if __name__ == '__main__':
    unittest.main()
