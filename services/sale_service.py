from services.json_handler import JsonStorage
from models.order import Order
from datetime import datetime


class SaleService:
    def __init__(self, car_service):
        self.storage = JsonStorage("orders.json")
        self.car_service = car_service
        self.orders = [Order(**o) for o in self.storage.load()]

    def create_sale(self, car_id, customer_id):
        # Шукаємо авто
        car = next((c for c in self.car_service.cars if c.id == car_id), None)
        if car and car.status == "Доступно":
            # Створюємо замовлення
            new_id = len(self.orders) + 1
            order = Order(new_id, car_id, customer_id, datetime.now().strftime("%Y-%m-%d"), car.price)

            # Міняємо статус машини
            car.status = "Продано"
            self.car_service.save()

            self.orders.append(order)
            self.save()
            return True
        return False

    def get_total_report(self):
        """Рахує загальну суму продажів для звіту"""
        return sum(float(order.total) for order in self.orders)

    def save(self):
        self.storage.save([o.to_dict() for o in self.orders])