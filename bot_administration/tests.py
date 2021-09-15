import unittest

import requests
from django.test import TestCase

from botseller_django_administration import settings


class TestBots(TestCase):
    def test_internet_working(self):
        """test internet connection"""
        url = "https://www.google.com"
        timeout = 5.
        try:
            request = requests.get(url, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as exception:
            self.fail("No internet connection.")

    def test_telegram_local_server_work(self):
        link = settings.TELEGRAM_ADDRESS

        try:
            data = requests.get(link, timeout=3)
        except Exception as e:
            print(type(e), e)
            self.fail("telegram server don't work")
        else:
            return data.text


if __name__ == '__main__':
    unittest.main()