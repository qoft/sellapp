from src.sellapp import Api

api = Api("API KEY")

# Get all products
products = api.get_all_products()
print(products)