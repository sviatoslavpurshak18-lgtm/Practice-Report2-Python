from services.json_handler import JsonStorage
from models.customer import Customer


class CustomerService:
    def __init__(self):
        self.storage = JsonStorage("customers.json")
        self.customers = [Customer(**c) for c in self.storage.load()]

    def save(self):
        self.storage.save([c.to_dict() for c in self.customers])

    def get_all(self):
        return self.customers

    def register_customer(self, customer: Customer):
        for c in self.customers:
            if c.email == customer.email:
                return False, "Користувач з таким email вже існує"
        customer.id = len(self.customers) + 1
        self.customers.append(customer)
        self.save()
        return True, "Реєстрація успішна"

    def login(self, email: str, password: str):
        self.customers = [Customer(**c) for c in self.storage.load()]
        for c in self.customers:
            if c.email == email and c.password == password:
                return c, "Успішно"
        return None, "Невірний email або пароль"