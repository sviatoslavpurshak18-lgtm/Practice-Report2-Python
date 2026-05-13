from storage.json_handler import JsonStorage
from models.car import Car


class CarService:
    def __init__(self):
        self.storage = JsonStorage("cars.json")
        self.cars = [Car(**c) for c in self.storage.load()]

    def add_car(self, brand, model, price, year, region, fuel, gearbox):
        new_id = max([c.id for c in self.cars], default=0) + 1

        car = Car(new_id, brand, model, price, year, region, fuel, gearbox)
        self.cars.append(car)
        self.save()

    def delete_car(self, car_id):
        self.cars = [c for c in self.cars if c.id != car_id]
        self.save()

    def save(self):
        self.storage.save([c.to_dict() for c in self.cars])

    def get_all(self):
        return self.cars

    def search_cars(self, brand="", model="", year_from=0, year_to=9999,
                    price_from=0, price_to=float("inf"), fuel="",
                    gearbox="", region="", status=""):
        result = []
        for car in self.cars:
            if brand and brand.lower() not in car.brand.lower(): continue
            if model and model.lower() not in car.model.lower(): continue
            if car.year < year_from or car.year > year_to: continue
            if car.price < price_from or car.price > price_to: continue
            if fuel and car.fuel != fuel: continue
            if gearbox and car.gearbox != gearbox: continue
            if region and car.region != region: continue
            if status and car.status != status: continue
            result.append(car)
        return result

    def get_models_by_brand(self, brand: str):
        return list(set(c.model for c in self.cars if c.brand == brand and c.model))

