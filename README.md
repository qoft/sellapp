
# sellapp

A Python SDK made for [sell.app](https://sell.app)

## Installation

```bash
  pip install sellapp
```

## Usage

### Basic usage

```python
import sellapp

api = sellapp.Api("Your api key")
blacklists = api.get_all_blacklists()
orders = api.get_all_orders()

print(blacklists)
print(orders)
```
