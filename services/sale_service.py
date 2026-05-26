from services.json_handler import JsonStorage
from models.order import Order


class SaleService:
    def __init__(self, car_service):
        self.storage = JsonStorage("orders.json")
        self.car_service = car_service
        self.orders = [Order(**o) for o in self.storage.load()]

    def create_sale(self, car_id, customer_id):
        car = next((c for c in self.car_service.cars if c.id == car_id), None)
        if car and car.status == "Доступно":
            new_id = len(self.orders) + 1
            order = Order(
                id=new_id,
                car_id=car_id,
                car_brand=car.brand,
                car_model=car.model,
                car_price=car.price,
                buyer_name="",
                buyer_phone="",
                buyer_email="",
            )
            car.status = "Продано"
            self.car_service.save()
            self.orders.append(order)
            self.save()
            return True
        return False

    def get_total_report(self):
        """Рахує загальну суму продажів для звіту"""
        return sum(float(order.car_price) for order in self.orders)

    def save(self):
        self.storage.save([o.to_dict() for o in self.orders])