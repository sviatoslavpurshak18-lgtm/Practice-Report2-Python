class Order:
    def __init__(self, id, car_id, car_brand, car_model, car_price,
                 buyer_name, buyer_phone, buyer_email, status="Нове"):
        self.id = id
        self.car_id = car_id
        self.car_brand = car_brand
        self.car_model = car_model
        self.car_price = car_price
        self.buyer_name = buyer_name
        self.buyer_phone = buyer_phone
        self.buyer_email = buyer_email
        self.status = status

    def to_dict(self):
        return self.__dict__