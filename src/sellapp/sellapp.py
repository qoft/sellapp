import httpx

# referencing https://github.com/t6c/sellapp-api-wrapper/blob/main/lib/api.js

class Api:
    def __init__(self, sellapp_api_key: str) -> None:
        self.sellapp_api_key = sellapp_api_key
        self.headers = {
            "Authorization": f"Bearer {self.sellapp_api_key}",
            "Accept": "application/json"
        }
        self.check_api_key()

    def do_request(self, params: str = "", json: dict = None, method: str = "GET") -> httpx.Response:
        """
        Do a request to the SellApp API

        :param params: The parameters of the request
        :param body: The body of the request
        :param method: The method of the request

        :return: The response of the request
        """
        return httpx.request(
            method=method, 
            url=f"https://sell.app/api/v1/{params}", 
            headers=self.headers,
            json=json
        )

    """
    
    All general functions
    
    """
    def check_api_key(self) -> None:
        """
        Check if the API key is valid
        """
        if self.do_request(params="listings").status_code in [401, 403]:
            raise ValueError("Invalid API key")
        


    """

    All blacklisting functions

    """
    def get_all_blacklists(self) -> dict:
        """
        Get all blacklists

        :return: All blacklists
        """
        return self.do_request(params="blacklists").json()

    def get_blacklist(self, id: str) -> dict:
        """
        Get a blacklist

        :param id: The ID of the blacklist

        :return: The blacklist
        """
        return self.do_requst(params=f"blacklists/{id}").json()

    def blacklist(self, blacklist_type: str, data: str, description: str) -> dict:
        """
        Blacklist a user

        :param blacklist_type: The type of the blacklist
        :param data: The data of the blacklist
        :param description: The description of the blacklist

        :return: The created blacklist
        """
        blacklist_type = blacklist_type.upper()
        if blacklist_type not in ["EMAIL", "IP", "COUNTRY"]:
            raise ValueError("Blacklist type is not \"EMAIL\", \"IP\", or \"COUNTRY\"")
        post_data = {
        	"type": blacklist_type,
        	"data": data,
        	"description": description
        }
        return self.do_request(params="blacklists", json=post_data, method="POST").json()

    def update_blacklist(self, id: str, blacklist_type: str, data: str, description: str) -> dict:
        blacklist_type = blacklist_type.upper()
        if blacklist_type not in ["EMAIL", "IP", "COUNTRY"]:
            raise ValueError("Blacklist type is not \"EMAIL\", \"IP\", or \"COUNTRY\"")
        post_data = {
			"type": blacklist_type,
			"data": data,
			"description": description
		}
        return self.do_request(params=f"blacklists/{id}", json=post_data, method="PATCH").json()

    def remove_blackist(self, id: str) -> dict:
        """
        Remove a blacklist

        :param id: The ID of the blacklist

        :return: The removed blacklist
        """
        return self.do_request(params=f"blacklists/{id}", method="DELETE").json()

    
    """
    
    All coupon functions
    
    """
    def get_all_coupons(self) -> dict:
        return self.do_request(params="coupons".json())

    def create_coupon(self, code: str, coupon_type: str, discount: str, store_wide: bool,  limit: int = None, expires_at: str = None) -> dict:
        """
        Create a coupon

        :param code: The code of the coupon
        :param coupon_type: The type of the coupon
        :param discount: The discount of the coupon
        :param store_wide: If the coupon is store wide
        :param limit: The limit of the coupon
        :param expires_at: The date the coupon expires at
        
        :return: The created coupon
        """
        post_data = {
            "code": code,
            "type": coupon_type,
            "discount": discount,
            "limit": limit,
            "store_wide": store_wide,
            "expires_at": expires_at
        }
        return self.do_request(params="coupons", json=post_data, method="POST").json()

    def get_coupon(self, id: str) -> dict:
        """
        Get a coupon

        :param id: The ID of the coupon

        :return: The coupon
        """
        return self.do_request(params=f"coupons/{id}").json()

    def update_coupon(self, id: str, code: str, coupon_type: str, discount: str, store_wide: bool,  limit: int = None, expires_at: str = None) -> dict:
        """
        Update a coupon
        :param id: The ID of the coupon
        :param code: The code of the coupon
        :param coupon_type: The type of the coupon
        :param discount: The discount of the coupon
        :param store_wide: If the coupon is store wide
        :param limit: The limit of the coupon
        :param expires_at: The date the coupon expires at
        
        :return: The updated coupon
        """
        payload = {
            "code": code,
            "type": coupon_type,
            "discount": discount,
            "limit": limit,
            "store_wide": store_wide,
            "expires_at": expires_at
        }
        return self.do_request(params=f"coupons/{id}", json=payload, method="PATCH").json()

    def delete_coupon(self, id: str) -> dict:
        """
        Delete a coupon

        :param id: The ID of the coupon

        :return: The deleted coupon
        """
        return self.do_request(params=f"coupons/{id}", method="DELETE").json()


    """

    All product functions

    """

    def get_all_products(self) -> dict:
        """
        Get all products

        :return: All products
        """
        return self.do_request(params="products").json()

    def get_all_orders_desc(self, field: str) -> dict:
        """
        Get all products in descending order

        :param field: field to query in descending order.

        :return: All products in descending order
        """
        post_data = {
        	"sort": [
        		{
        			field: field,
        			"direction": "desc", 
        		}
        	]
        }
        return self.do_request(params="invoices/search", json=post_data).json()

    def get_product(self, id: str) -> dict:
        """
        Get a product

        :param id: The ID of the product

        :return: The product
        """
        return self.do_request(params=f"listings/{id}").json()

    def create_product(self, post_data: dict = None) -> dict:
        """
        Create a product
        Post data found here: https://developer.sell.app/#tag/Products-(v1)/paths/~1api~1v1~1listings/post

        :param post_data: The data of the product

        :return: The created product
        """
        if post_data is None:
            raise ValueError("Post data is None, please provide post data found here: https://developer.sell.app/#tag/Products-(v1)/paths/~1api~1v1~1listings/post")
        return self.do_request(params="listings", json=post_data, method="POST").json()

    def update_product(self, id: str, post_data: dict = None) -> dict:
        """
        Update a product
        Post data found here: https://developer.sell.app/#tag/Products-(v1)/paths/~1api~1v1~1listings~1%7Blisting%7D/patch

        :param id: The ID of the product
        :param post_data: The data of the product

        :return: The updated product
        """
        if post_data is None:
            raise ValueError("Post data is None, please provide post data found here: https://developer.sell.app/#tag/Products-(v1)/paths/~1api~1v1~1listings~1%7Blisting%7D/patch")
        return self.do_request(params=f"listings/{id}", json=post_data, method="PATCH").json()

    def delete_product(self, id: str) -> dict:
        """
        Delete a product

        :param id: The ID of the product

        :return: The deleted product
        """
        return self.do_request(params=f"listings/{id}", method="DELETE").json()

    
    """
    
    ALl section functions
    
    """
    def get_all_sections(self) -> dict:
        """
        Get all sections

        :return: All sections
        """
        return self.do_request(params="sections").json()

    def get_section(self, id: str) -> dict:
        """
        Get a section

        :param id: The ID of the section

        :return: The section
        """
        return self.do_request(params=f"sections/{id}").json()

    def create_section(self, title: str, hidden: bool, order: int = 0) -> dict:
        """
        Create a section

        :param title: The title of the section
        :param hidden: If the section is hidden
        :param order: The order of the section

        :return: The created section
        """
        return self.do_request(params="sections", json={"title": title, "hidden": hidden, "order": order}, method="POST").json()

    def update_section(self, id: str, post_data: dict = None) -> dict:
        """
        Update a section
        Post data found here: https://developer.sell.app/#tag/Sections/paths/~1api~1v1~1sections~1%7Bsection%7D/patch

        :param id: The ID of the section
        :param post_data: The data of the section

        :return: The updated section
        """
        if post_data is None:
            raise ValueError("Post data is None, please provide post data found here: https://developer.sell.app/#tag/Sections/paths/~1api~1v1~1sections~1%7Bsection%7D/patch")
        return self.do_request(params=f"sections/{id}", json=post_data, method="PATCH").json()

    def delete_section(self, id: str) -> dict:
        """
        Delete a section

        :param id: The ID of the section

        :return: The deleted section
        """
        return self.do_request(params=f"sections/{id}", method="DELETE").json()

    """
    
    All feedback functions
    
    """
    def get_all_feedback(self) -> dict:
        """
        Get all feedback

        :return: All feedback
        """
        return self.do_request(params="feedback").json()

    def get_feedback(self, id: str) -> dict:
        """
        Get a feedback

        :param id: The ID of the feedback

        :return: The feedback
        """
        return self.do_request(params=f"feedback/{id}").json()

    def reply_feedback(self, id: str, message: str) -> dict:
        """
        Reply to a feedback

        :param id: The ID of the feedback
        :param message: The message to reply with

        :return: The replied feedback
        """
        return self.do_request(params=f"feedback/{id}", json={"reply": message}, method="PATCH").json()


    """
    
    All order functions
    
    """
    def get_all_orders(self) -> dict:
        """
        Get all orders

        :return: All orders
        """
        return self.do_request(params="invoices").json()

    def get_order(self, id: str) -> dict:
        """
        Get a order

        :param id: The ID of the order

        :return: The order
        """
        return self.do_request(params=f"invoices/{id}").json()

    def create_invoice(self, customer_email: str, total: str, payment_method: str, coupon: str, products: dict) -> dict:
        """
        Create a invoice

        :param customer_email: The email of the customer who placed this order.
        :param total: The total amount to pay for this order.
        :param payment_method: The payment gateway to process this order with.
        :param coupon: The coupon code to apply to this order.
        :param object: The object of the invoice

        :return: The created invoice
        """
        return self.do_request(
            params="invoices", 
            json={
                "customer_email": customer_email, 
                "total": total, 
                "payment_method": payment_method, 
                "coupon": coupon, 
                "products": products
            }, method="POST").json()
    
    def issue_replacement(self, id: int, listings: list = None) -> dict:
        """
        Issue a replacement

        :param id: The ID of the order
        :param listings: The listings to replace

        :return: The replaced invoice
        """

        if listings is None:
            listings = []
        return self.do_request(params=f"invoices/{id}/issue-replacement", json={"listings": listings}, method="PATCH").json()

    def create_payment(self, id: int) -> dict:
        """
        Create a payment

        :param id: The ID of the order

        :return: The payment
        """
        return self.do_request(params=f"invoices/{id}/checkout", method="POST").json()

    """
    
    All ticket functions
    
    """
    def get_all_tickets(self) -> dict:
        """
        Get all tickets

        :return: All tickets
        """
        return self.do_request(params="tickets").json()

    def get_ticket(self, id: str) -> dict:
        """
        Get a ticket

        :param id: The ID of the ticket

        :return: The ticket
        """
        return self.do_request(params=f"tickets/{id}").json()

    def get_all_ticket_messages(self, id: str) -> dict:
        """
        Get all ticket messages

        :param id: The ID of the ticket

        :return: All ticket messages
        """
        return self.do_request(params=f"tickets/{id}/messages").json()
    
    def get_ticket_message(self, id: str, message_id: str) -> dict:
        """
        Get a ticket message

        :param id: The ID of the ticket
        :param message_id: The ID of the message

        :return: The ticket message
        """
        return self.do_request(params=f"tickets/{id}/messages/{message_id}").json()

    def respond_ticket(self, id: str, message: str, author: str = None) -> dict:
        """
        Respond to a ticket

        :param id: The ID of the ticket
        :param message: The message to respond with

        :return: The responded ticket
        """
        post_data = {"content": message}
        if author is not None:
            if author.upper() not in ["CUSTOMER", "STORE"]:
                raise ValueError("Author must be either customer or store.")
            post_data["author"] = author.upper()

        return self.do_request(params=f"tickets/{id}/messages", json=post_data, method="POST").json()

