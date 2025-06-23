import base64
import json
import logging
import random
import time
from typing import Dict

import httpx
import jwt


class NetoSecret:
    @staticmethod
    def encode(api_key: Dict[str, str]) -> str:
        api_key_json = json.dumps(api_key)
        api_key_base64 = base64.b64encode(api_key_json.encode()).decode()
        return api_key_base64

    @staticmethod
    def decode(api_key_base64: str) -> Dict[str, str]:
        api_key_json = base64.b64decode(api_key_base64).decode()
        api_key = json.loads(api_key_json)
        return api_key


class NetoAPI:
    def __init__(self, netosecret: str) -> None:
        """
        Initialize the NetoAPI class.
        This class is responsible for handling authentication and API requests to the Netography Fusion API.
        """
        self.subaccount = None
        self.token = None
        self.token_expires_in = 0

        self.netosecret = NetoSecret.decode(netosecret)
        self.NETO_BASE_URL = self.netosecret.get("url")

        if "/api/v1" in self.NETO_BASE_URL:
            self.NETO_BASE_URL = self.NETO_BASE_URL.replace("/api/v1", "")

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _create_jwt_request_token(self) -> str:
        payload = {
            "iat": int(time.time()),
            "jti": str(random.randint(0, 100000000)),
            "appname": self.netosecret.get("appname"),
            "appkey": self.netosecret.get("appkey"),
            "shortname": self.netosecret.get("shortname"),
        }
        token = jwt.encode(
            payload, self.netosecret.get("sharedsecret"), algorithm="HS256"
        )
        return token

    def authenticate(self) -> str | None:
        if self.token is None:
            logging.info(f"Authenticating to Netography Fusion API as customer {self.netosecret.get('shortname')}")
            if self.netosecret.get("appname") is None:
                logging.error("appname not set")
            if self.netosecret.get("shortname") is None:
                logging.error("shortname not set")
            if self.netosecret.get("appkey") is None:
                logging.error("appkey not set")
            if self.netosecret.get("sharedsecret") is None:
                logging.error("shared_secret not set")
            if (
                self.netosecret.get("appname") is None
                or self.netosecret.get("shortname") is None
                or self.netosecret.get("appkey") is None
                or self.netosecret.get("sharedsecret") is None
            ):
                raise Exception(
                    "Netography Fusion API credentials are not set properly"
                )

            jwt_request_token = self._create_jwt_request_token()

            try:
                body = {"jwt": jwt_request_token}
                response = httpx.post(
                    f"{self.NETO_BASE_URL}/api/v1/auth/token",
                    json=body,
                    headers=self.headers,
                )
                response.raise_for_status()  # Raise an error for bad responses
                if response.status_code == 200:
                    response_json = response.json()
                    self.token = response_json["access_token"]
                    self.headers["Authorization"] = f"Bearer {self.token}"
                    logging.info("Successfully authenticated to Netography Fusion API")
                    return self.token
            except httpx.HTTPStatusError as e:
                logging.error(logging.exception(e))
                logging.error(
                    f"Failed to authenticate to Netography Fusion API: {e.response.text}"
                )
                raise Exception("Unable to authenticate to Netography Fusion API")
        return self.token
