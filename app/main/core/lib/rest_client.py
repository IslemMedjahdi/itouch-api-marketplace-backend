import requests
from typing import Dict, Tuple


class RestClient:
    def get(self, url, headers) -> Tuple[Dict, int]:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json(), response.status_code

    def post(self, url, headers, data) -> Tuple[Dict, int]:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        return response.json(), response.status_code

    def delete(self, url, headers) -> Tuple[Dict, int]:
        response = requests.delete(url, headers=headers, timeout=10)
        return response.json(), response.status_code

    def patch(self, url, headers, data) -> Tuple[Dict, int]:
        response = requests.patch(url, headers=headers, data=data, timeout=10)
        return response.json(), response.status_code
