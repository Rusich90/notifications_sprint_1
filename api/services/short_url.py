import time
from functools import lru_cache

import requests
from requests.structures import CaseInsensitiveDict

from config.settings import URLSettings

config = URLSettings()


class ShortUrl:
    def __init__(self):
        self.url = config.api_url
        self.redirect_url = config.redirect_url
        self.token = config.token.get_secret_value()
        self.lifetime = config.lifetime_minutes
        self.domain = config.domain

    def _get_headers(self):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {self.token}"
        headers["Content-Type"] = "application/json"
        return headers

    def _get_data(self, user_id):
        timestamp = time.time() + (60 * self.lifetime)
        data = {
            "domain": self.domain,
            "long_url": f"{self.redirect_url}?id={user_id}&timestamp={timestamp}"
        }
        return data

    def get_short_url(self, user_id):
        headers = self._get_headers()
        data = self._get_data(user_id)
        resp = requests.post(self.url, headers=headers, json=data)
        return resp.json()['link']


@lru_cache()
def get_short_url_service() -> ShortUrl:
    return ShortUrl()
