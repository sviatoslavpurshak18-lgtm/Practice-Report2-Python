class Car:
    def __init__(self, id, brand, model, price, year, region="Не вказано",
                 fuel="Не вказано", gearbox="Не вказано", status="Доступно",
                 mileage=0, city="", body_type="", image=""):
        self.id = id
        self.brand = brand
        self.model = model
        self.price = price
        self.year = year
        self.region = region
        self.fuel = fuel
        self.gearbox = gearbox
        self.status = status
        self.mileage = mileage
        self.city = city
        self.body_type = body_type
        self.image = image

    def to_dict(self):
        return self.__dict__