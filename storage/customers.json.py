from storage.json_handler import JsonStorage
from models.customer import Customer


class CustomerService:
    def __init__(self):
        self.storage = JsonStorage("customers.json")
        self.customers = [Customer(**c) for c in self.storage.load()]

    def login(self, email, password):
        for c in self.customers:
            if c.email == email and c.password == password:
                return c, "Успішно"
        return None, "Помилка входу"

    def register_customer(self, customer_obj):
        if any(c.email == customer_obj.email for c in self.customers):
            return False, "Email зайнятий"

        customer_obj.id = len(self.customers) + 1
        self.customers.append(customer_obj)
        self.save()
        return True, "Готово"

    def save(self):
        self.storage.save([c.__dict__ for c in self.customers])