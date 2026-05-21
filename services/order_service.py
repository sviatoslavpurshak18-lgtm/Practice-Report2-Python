from services.json_handler import JsonStorage
from models.order import Order

class OrderService:
    def __init__(self):
        self.storage = JsonStorage("orders.json")
        self.orders = [Order(**o) for o in self.storage.load()]

    def add_order(self, car_id, car_brand, car_model, car_price,
                  buyer_name, buyer_phone, buyer_email):
        new_id = max([o.id for o in self.orders], default=0) + 1
        order = Order(
            id=new_id,
            car_id=car_id,
            car_brand=car_brand,
            car_model=car_model,
            car_price=car_price,
            buyer_name=buyer_name,
            buyer_phone=buyer_phone,
            buyer_email=buyer_email,
        )
        self.orders.append(order)
        self.save()
        return order

    def get_all(self):
        return self.orders

    def save(self):
        self.storage.save([o.to_dict() for o in self.orders])