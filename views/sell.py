import flet as ft
from services.car_service import CarService

RED   = "#e8192c"
WHITE = "#ffffff"
BG    = "#f0f2f5"
DARK  = "#1a1a2e"
GREY  = "#8a8fa8"
LGREY = "#d4d8e6"

MODELS = {
    "BMW": ["3 Series", "5 Series", "7 Series", "X1", "X3", "X5", "X6", "M3", "M5"],
    "Mercedes-Benz": ["C-Class", "E-Class", "S-Class", "GLC", "GLE", "GLS", "A-Class", "CLA"],
    "Audi": ["A3", "A4", "A6", "A8", "Q3", "Q5", "Q7", "Q8", "TT", "RS6"],
    "Toyota": ["Camry", "Corolla", "RAV4", "Land Cruiser", "Highlander", "Yaris", "Prius"],
    "Volkswagen": ["Golf", "Passat", "Tiguan", "Touareg", "Polo", "Jetta", "T-Roc"],
    "Honda": ["Civic", "Accord", "CR-V", "HR-V", "Pilot", "Jazz"],
    "Hyundai": ["Tucson", "Santa Fe", "Elantra", "i30", "Sonata", "Creta", "Ioniq"],
    "Kia": ["Sportage", "Sorento", "Ceed", "Stinger", "Telluride", "Rio", "Niro"],
    "Ford": ["Focus", "Mondeo", "Kuga", "Explorer", "Mustang", "Ranger", "F-150"],
    "Chevrolet": ["Cruze", "Malibu", "Equinox", "Traverse", "Camaro", "Silverado"],
    "Mazda": ["Mazda3", "Mazda6", "CX-3", "CX-5", "CX-9", "MX-5"],
    "Skoda": ["Octavia", "Superb", "Fabia", "Kodiaq", "Karoq", "Scala"],
    "Renault": ["Megane", "Logan", "Duster", "Captur", "Kadjar", "Scenic"],
    "Opel": ["Astra", "Insignia", "Mokka", "Crossland", "Grandland", "Corsa"],
    "Nissan": ["Qashqai", "X-Trail", "Juke", "Leaf", "Navara", "Micra"],
}
BRANDS = list(MODELS.keys())
BODY_TYPES = ["Седан","Хетчбек","Позашляховик","Кросовер","Мінівен","Купе","Пікап"]
FUELS      = ["Бензин","Дизель","Електро","Гібрид","Газ"]
GEARS      = ["Автомат","Механіка","Робот","Варіатор"]
YEARS      = [str(y) for y in range(2025, 1989, -1)]
REGIONS    = ["Київська","Харківська","Дніпропетровська","Одеська","Запорізька",
               "Львівська","Вінницька","Полтавська","Черкаська","Тернопільська"]
CITIES     = ["Київ","Харків","Дніпро","Одеса","Запоріжжя",
               "Львів","Вінниця","Полтава","Черкаси","Тернопіль"]
TYPES      = ["Легкові","Вантажівки","Мото","Автобуси"]


class SellView:
    def __init__(self, page: ft.Page, user=None, on_back=None):
        self.page = page
        self.user = user
        self.on_back = on_back
        self.svc = CarService()

    def _dd(self, label, options, width=480, required=True):
        mark = ft.Text(" *", color=RED, size=13) if required else ft.Container()
        dd = ft.Dropdown(
            hint_text="Оберіть",
            options=[ft.dropdown.Option(o) for o in options],
            width=width, bgcolor=WHITE, border_color=LGREY,
            border_radius=8, color=DARK,
            hint_style=ft.TextStyle(color=GREY, size=13),
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
        )
        return ft.Row([
            ft.Container(ft.Text(label, size=14, color=DARK), width=160),
            mark,
            dd,
        ], spacing=4), dd

    def _tf(self, label, hint="", required=False, width=480):
        mark = ft.Text(" *", color=RED, size=13) if required else ft.Container()
        tf = ft.TextField(
            hint_text=hint, width=width, bgcolor=WHITE,
            border_color=LGREY, border_radius=8, color=DARK,
            hint_style=ft.TextStyle(color=GREY, size=13),
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
            text_size=13,
        )
        return ft.Row([
            ft.Container(ft.Text(label, size=14, color=DARK), width=160),
            mark,
            tf,
        ], spacing=4), tf

    def build(self):
        self.page.clean()
        self.page.bgcolor = BG

        type_row,   self.dd_type   = self._dd("Тип транспорту", TYPES)
        brand_row,  self.dd_brand  = self._dd("Марка авто", BRANDS)
        model_row,  self.dd_model  = self._dd("Модель авто", [])
        year_row,   self.dd_year   = self._dd("Рік випуску", YEARS, width=200)
        body_row,   self.dd_body   = self._dd("Тип кузова", BODY_TYPES)
        fuel_row,   self.dd_fuel   = self._dd("Пальне", FUELS, required=False)
        gear_row,   self.dd_gear   = self._dd("Коробка передач", GEARS, required=False)
        region_row, self.dd_region = self._dd("Регіон", REGIONS)
        city_row,   self.dd_city   = self._dd("Місто", CITIES)
        miles_row,  self.tf_miles  = self._tf("Пробіг", hint="тис.км")
        mod_row,    self.tf_mod    = self._tf("Модифікація", hint="Модифікація")
        price_row,  self.tf_price  = self._tf("Ціна $", hint="Введіть ціну", required=True)

        self.dd_brand.on_change = self.brand_changed
        self.err_text = ft.Text("", color=RED, size=13)

        # Navbar
        navbar = ft.Container(
            content=ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, icon_color=DARK,
                              on_click=lambda e: self.on_back() if self.on_back else None),
                ft.Row([
                    ft.Container(content=ft.Text("auto", size=17,
                                                  weight=ft.FontWeight.BOLD, color=WHITE),
                                 bgcolor=RED, border_radius=4,
                                 padding=ft.padding.symmetric(horizontal=8, vertical=3)),
                    ft.Container(content=ft.Text("RIA", size=17,
                                                  weight=ft.FontWeight.BOLD, color=WHITE),
                                 bgcolor="#003580", border_radius=4,
                                 padding=ft.padding.symmetric(horizontal=8, vertical=3)),
                ], spacing=2),
                ft.Text("Розмістити оголошення", size=15,
                        weight=ft.FontWeight.BOLD, color=DARK),
                ft.Container(expand=True),
                ft.Text(f"👤 {self.user.name}" if self.user else "", size=13, color=GREY),
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=WHITE,
            padding=ft.padding.symmetric(horizontal=24, vertical=12),
            shadow=ft.BoxShadow(blur_radius=6, color="#10000000", offset=ft.Offset(0, 2)),
        )

        form = ft.Container(
            content=ft.Column([
                ft.Text("Додати оголошення", size=20,
                        weight=ft.FontWeight.BOLD, color=DARK),
                ft.Divider(color=LGREY),
                type_row, brand_row, model_row, year_row,
                miles_row, body_row, mod_row,
                region_row, city_row,
                fuel_row, gear_row,
                price_row,
                self.err_text,
                ft.Container(height=8),
                ft.ElevatedButton(
                    "📤  Опублікувати оголошення",
                    width=660,
                    style=ft.ButtonStyle(
                        bgcolor=RED, color=WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.padding.symmetric(vertical=14),
                        text_style=ft.TextStyle(size=15, weight=ft.FontWeight.W_600),
                    ),
                    on_click=self.submit,
                ),
            ], spacing=12, scroll=ft.ScrollMode.AUTO),
            bgcolor=WHITE, border_radius=16, padding=28,
            shadow=ft.BoxShadow(blur_radius=12, color="#12000000", offset=ft.Offset(0, 4)),
        )

        self.page.add(
            navbar,
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=form,
                        padding=ft.padding.symmetric(horizontal=32, vertical=24),
                    )
                ], scroll=ft.ScrollMode.AUTO),
                expand=True, bgcolor=BG,
            )
        )

    def brand_changed(self, e):
        models = MODELS.get(self.dd_brand.value or "", [])
        self.dd_model.options = [ft.dropdown.Option(m) for m in models]
        self.dd_model.value = None
        self.page.update()

    def submit(self, e):
        required = [
            (self.dd_type,   "Тип транспорту"),
            (self.dd_brand,  "Марка"),
            (self.dd_model,  "Модель"),
            (self.dd_year,   "Рік"),
            (self.dd_body,   "Тип кузова"),
            (self.dd_region, "Регіон"),
            (self.dd_city,   "Місто"),
            (self.tf_price,  "Ціна"),
        ]
        missing = [name for field, name in required if not field.value]
        if missing:
            self.err_text.value = f"Заповніть: {', '.join(missing)}"
            self.page.update()
            return
        try:
            price = float(self.tf_price.value.replace(",", "."))
            miles = int(self.tf_miles.value or "0")
        except ValueError:
            self.err_text.value = "Ціна або пробіг мають бути числами"
            self.page.update()
            return

        self.svc.add_car(
            brand=self.dd_brand.value,
            model=self.dd_model.value,
            price=price,
            year=int(self.dd_year.value),
            region=self.dd_region.value,
            fuel=self.dd_fuel.value or "",
            gearbox=self.dd_gear.value or "",
        )

        self.err_text.color = "#27ae60"
        self.err_text.value = "✅ Оголошення успішно розміщено!"
        self.page.update()