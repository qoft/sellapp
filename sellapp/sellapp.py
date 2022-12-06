import requests
import json
import typing
from typing import Iterable


class Api:
    def __init__(self, sellapp_api_key: str) -> None:
        self.sellapp_api_key = sellapp_api_key
        self.headers = {
            "Authorization": f"Bearer {self.sellapp_api_key}",
            "Accept": "application/json"
        }

    def do_request(params: str = "", body: str | dict = None, method: str = "GET") -> requests.Response:
        return requests.request(
            method=method, 
            url=f"https://sell.app/api/v1/{params}", 
            headers=self.headers,
            json=body
        )

    """

    All blacklisting functions

    """
    def get_all_blacklists() -> dict:
        return self.do_request(params=f"blacklists").json()

    def get_blacklist(id: str) -> dict:
        return self.do_requst(params=f"blacklists/{id}").json()

    def blacklist(blacklist_type: str, data: str, description: str) -> dict:
        blacklist_type = blacklist_type.upper()
        if blacklist_type not in ["EMAIL", "IP", "COUNTRY"]:
            raise ValueError("Blacklist type is not \"EMAIL\", \"IP\", or \"COUNTRY\"")
        post_data = {
			"type": blacklist_type,
			"data": data,
			"description": description
		}
        return self.do_request(params=f"blacklists", body=post_data, method="POST").json()

    def update_blacklist(id: str, blacklist_type: str, data: str, description: str) -> dict:
        blacklist_type = blacklist_type.upper()
        if blacklist_type not in ["EMAIL", "IP", "COUNTRY"]:
            raise ValueError("Blacklist type is not \"EMAIL\", \"IP\", or \"COUNTRY\"")
        post_data = {
			"type": blacklist_type,
			"data": data,
			"description": description
		}
        return self.do_request(params=f"blacklists/{id}", body=post_data, method="PATCH").json()

    def remove_blackist(id: str) -> dict:
        return self.do_request(params=f"blacklists/{id}", method="DELETE").json()

    
    """
    
    All coupon functions
    
    """
    def get_all_coupons() -> dict:
        return self.do_request(params="coupons".json())

    def create_coupon(code: str, coupon_type: str, discount: str, store_wide: bool,  limit: int = None, expires_at: str = None) -> dict:
        payload = {
            "code": code,
            "type": coupon_type,
            "discount": discount,
            "limit": limit,
            "store_wide": store_wide,
            "expires_at": expires_at
        }
        return self.do_request(params="coupons", body=payload, method="POST").json()


    