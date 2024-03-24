# flake8: noqa

from app.main.core.lib.rest_client import RestClient


class ChargilyApi:
    def __init__(self, rest_client: RestClient):
        self.api_url = "https://pay.chargily.net/test/api/v2"
        self.secret_key = "test_sk_fCFpkasB82ryTSEGrQKgowjJn2YfgGlrZZ8lsQFU"  # TODO: add this to env variables
        self.rest_client = rest_client

    def create_product(self, product_name: str, product_description: str) -> str | None:
        data = {"name": product_name, "description": product_description}

        try:
            response, status = self.rest_client.post(
                url=self.api_url + "/products",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.secret_key}",
                },
                data=data,
            )
            print(response)
            return response.get("id")
        except Exception as e:
            print(e)
            return None

    def create_price(self, product_id: str, amount: int) -> str | None:
        data = {"product_id": product_id, "amount": amount, "currency": "dzd"}

        try:
            response, status = self.rest_client.post(
                self.api_url + "/prices",
                {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.secret_key}",
                },
                data=data,
            )
            return response.get("id")
        except Exception:
            return None
