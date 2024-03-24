import hmac
import hashlib

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

    def create_checkout(
        self, price_id: str, redirect_url: str, metadata: dict
    ) -> str | None:
        data = {
            "items": [{"price": price_id, "quantity": 1}],
            "success_url": redirect_url,
            "metadata": {
                "user_id": metadata.get("user_id"),
                "api_id": metadata.get("api_id"),
                "plan_name": metadata.get("plan_name"),
            },
        }
        try:
            response, status = self.rest_client.post(
                self.api_url + "/checkouts",
                {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.secret_key}",
                },
                data=data,
            )
            return response.get("checkout_url")
        except Exception as e:
            print(e)
            return None

    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        computed_signature = hmac.new(
            self.secret_key.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, computed_signature):
            return False

        return True
