class Order:
    def __init__(self, id, car_id, customer_id, date, total):
        self.id = id
        self.car_id = car_id
        self.customer_id = customer_id
        self.date = date
        self.total = total

    def to_dict(self):
        return self.__dict__