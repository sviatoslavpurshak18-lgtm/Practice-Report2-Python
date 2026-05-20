import flet as ft
from services.car_service import CarService
from services.order_service import OrderService

RED   = "#e8192c"
WHITE = "#ffffff"
BG    = "#f0f2f5"
DARK  = "#1a1a2e"
GREY  = "#8a8fa8"
LGREY = "#d4d8e6"

MODELS = {
    "BMW": ["3 Series","5 Series","7 Series","X1","X3","X5","X6","M3","M5"],
    "Mercedes-Benz": ["C-Class","E-Class","S-Class","GLC","GLE","GLS","A-Class","CLA"],
    "Audi": ["A3","A4","A6","A8","Q3","Q5","Q7","Q8","TT","RS6"],
    "Toyota": ["Camry","Corolla","RAV4","Land Cruiser","Highlander","Yaris","Prius"],
    "Volkswagen": ["Golf","Passat","Tiguan","Touareg","Polo","Jetta","T-Roc"],
    "Honda": ["Civic","Accord","CR-V","HR-V","Pilot","Jazz"],
    "Hyundai": ["Tucson","Santa Fe","Elantra","i30","Sonata","Creta","Ioniq"],
    "Kia": ["Sportage","Sorento","Ceed","Stinger","Telluride","Rio","Niro"],
    "Ford": ["Focus","Mondeo","Kuga","Explorer","Mustang","Ranger","F-150"],
    "Chevrolet": ["Cruze","Malibu","Equinox","Traverse","Camaro","Silverado"],
    "Mazda": ["Mazda3","Mazda6","CX-3","CX-5","CX-9","MX-5"],
    "Skoda": ["Octavia","Superb","Fabia","Kodiaq","Karoq","Scala"],
    "Renault": ["Megane","Logan","Duster","Captur","Kadjar","Scenic"],
    "Opel": ["Astra","Insignia","Mokka","Crossland","Grandland","Corsa"],
    "Nissan": ["Qashqai","X-Trail","Juke","Leaf","Navara","Micra"],
}
MODELS_TRUCKS = {
    "Mercedes-Benz Trucks": ["Actros","Atego","Arocs","Sprinter"],
    "MAN": ["TGX","TGS","TGM","TGL"],
    "Volvo Trucks": ["FH","FM","FMX","FL","FE"],
    "Scania": ["R Series","S Series","G Series","P Series"],
    "DAF": ["XF","CF","LF"],
    "Iveco": ["Stralis","Eurocargo","Daily"],
    "Renault Trucks": ["T Series","C Series","K Series","D Series"],
    "КАМАЗ": ["5490","65115","6520","43118"],
    "ГАЗ": ["Газель Next","Газель Business","Газон Next"],
    "Богдан": ["E-1","A-069","A-092"],
}
MODELS_MOTORCYCLES = {
    "Yamaha": ["R1","R6","MT-07","MT-09","Tracer 9"],
    "Honda": ["CBR600RR","CB500","Africa Twin","Gold Wing"],
    "Kawasaki": ["Ninja 400","Ninja ZX-6R","Z900","Versys 650"],
    "Suzuki": ["GSX-R600","V-Strom 650","Hayabusa","SV650"],
    "BMW Motorrad": ["S1000RR","R1250GS","F900R","K1600"],
    "Ducati": ["Panigale V4","Monster","Multistrada","Scrambler"],
    "KTM": ["Duke 390","RC 390","1290 Super Duke","Adventure 890"],
    "Harley-Davidson": ["Sportster","Street Glide","Fat Boy","Iron 883"]
}
MODELS_BUSES = {
    "Mercedes-Benz": ["Sprinter Bus","Tourismo","Citaro"],
    "MAN": ["Lion's Coach","Lion's City","RR8"],
    "Volvo": ["9700","7900","9800"],
    "Scania": ["Touring","Citywide","Interlink"],
    "Neoplan": ["Cityliner","Skyliner","Tourliner"],
    "Богдан": ["A-069","A-092","A-144"],
    "Еталон": ["A081","A084","A111"],
    "IVECO": ["Crossway","Evadys","Daily Bus"]
}
FUELS = ["Бензин", "Дизель", "Електро", "Гібрид", "Газ", "Бензин + Газ (ГБО)",
         "Плагін-гібрид", "Водень", "Біопаливо", "Метан", "Пропан", "Етанол"]
GEARS   = ["Автомат","Механіка","Робот","Варіатор"]
REGIONS = [
    "Вінницька", "Волинська", "Дніпропетровська", "Житомирська",
    "Закарпатська", "Івано-Франківська", "Київська", "Кіровоградська",
    "Львівська", "Миколаївська", "Одеська", "Полтавська",
    "Рівненська", "Сумська", "Тернопільська", "Харківська",
    "Хмельницька", "Черкаська", "Чернівецька", "Чернігівська"
]
TYPES = ["Легкові", "Вантажівки", "Мотоцикли", "Автобуси"]


def _trigger(label_ctrl, on_click, width=220):
    return ft.Container(
        content=ft.Row([
            label_ctrl,
            ft.Container(expand=True),
            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=GREY, size=18),
        ]),
        bgcolor=WHITE, border_radius=8,
        border=ft.border.all(1, LGREY),
        padding=ft.padding.symmetric(horizontal=14, vertical=10),
        width=width, on_click=on_click,
    )


class MainView:
    def __init__(self, page: ft.Page, on_sell=None, on_logout=None, current_user=None):
        self.page = page
        self.car_service = CarService()
        self.order_service = OrderService()
        self.on_sell = on_sell
        self.on_logout = on_logout
        self.current_user = current_user
        self.page.title = "AutoUA — Система продажу автомобілів"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = BG
        self.page.padding = 0

    def build(self):
        self.page.clean()

        self.selected_brand  = {"v": ""}
        self.selected_models = {"v": []}
        self._current_models = MODELS
        self.year_from = {"v": ""}
        self.year_to   = {"v": ""}

        self.dd_type = ft.Dropdown(
            label="Тип транспорту", width=200,
            options=[ft.dropdown.Option(t) for t in TYPES],
            bgcolor=WHITE, border_color=LGREY, color=DARK, text_size=14,
        )
        self.dd_fuel = ft.Dropdown(
            label="Пальне", width=200,
            options=[ft.dropdown.Option(f) for f in FUELS],
            bgcolor=WHITE, border_color=LGREY, color=DARK, text_size=14,
        )
        self.dd_gear = ft.Dropdown(
            label="Коробка передач", width=200,
            options=[ft.dropdown.Option(g) for g in GEARS],
            bgcolor=WHITE, border_color=LGREY, color=DARK, text_size=14,
        )
        self.dd_region = ft.Dropdown(
            label="Регіон", width=200,
            options=[ft.dropdown.Option(r) for r in REGIONS],
            bgcolor=WHITE, border_color=LGREY, color=DARK, text_size=14,
        )

        self._init_brand_picker()
        self._init_year_picker()
        self._init_price_picker()

        brand_picker = self._make_brand_stack()
        year_picker  = self._make_year_stack()
        price_picker = self._make_price_stack()

        filters_block = ft.Container(
            content=ft.Column([
                ft.Text("Знаємо, бо перевірили", size=26,
                        weight=ft.FontWeight.BOLD, color=DARK),
                ft.Row([
                    self.dd_type,
                    brand_picker,
                    year_picker,
                    price_picker,
                ], spacing=12, wrap=True),
                ft.Row([
                    self.dd_region,
                    self.dd_fuel,
                    self.dd_gear,
                ], spacing=12),
                ft.Button(
                    "Шукати", width=220,
                    style=ft.ButtonStyle(
                        bgcolor=RED, color=WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.padding.symmetric(vertical=16),
                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600),
                    ),
                    on_click=self.do_search,
                ),
            ], spacing=16),
            bgcolor=WHITE, border_radius=16, padding=28,
            margin=ft.margin.symmetric(horizontal=32, vertical=16),
            shadow=ft.BoxShadow(blur_radius=10, color="#12000000", offset=ft.Offset(0, 2)),
        )

        if self.current_user:
            right = ft.Row([
                ft.Text(f"👤 {self.current_user.name}", size=13,
                        color=DARK, weight=ft.FontWeight.W_500),
                ft.TextButton("Вийти",
                    on_click=lambda e: self.on_logout() if self.on_logout else None,
                    style=ft.ButtonStyle(color=GREY)),
                ft.ElevatedButton("+ Продати авто",
                    on_click=lambda e: self.on_sell() if self.on_sell else None,
                    style=ft.ButtonStyle(bgcolor=RED, color=WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.symmetric(horizontal=16, vertical=9))),
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        else:
            right = ft.ElevatedButton("+ Продати авто",
                on_click=lambda e: self.on_sell() if self.on_sell else None,
                style=ft.ButtonStyle(bgcolor=RED, color=WHITE,
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.padding.symmetric(horizontal=16, vertical=9)))

        navbar = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Text("auto", size=17, weight=ft.FontWeight.BOLD, color=WHITE),
                        bgcolor=RED, border_radius=4,
                        padding=ft.padding.symmetric(horizontal=8, vertical=3)),
                    ft.Container(
                        content=ft.Text("UA", size=17, weight=ft.FontWeight.BOLD, color=WHITE),
                        bgcolor="#003580", border_radius=4,
                        padding=ft.padding.symmetric(horizontal=8, vertical=3)),
                ], spacing=2),
                ft.Container(expand=True),
                right,
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=WHITE,
            padding=ft.padding.symmetric(horizontal=32, vertical=12),
            shadow=ft.BoxShadow(blur_radius=6, color="#15000000", offset=ft.Offset(0, 2)),
        )

        self.count_text = ft.Text("", size=13, color=GREY, italic=True)
        self.car_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=12)

        self.page.add(
            navbar,
            ft.Container(bgcolor=BG, expand=True, content=ft.Column([
                filters_block,
                ft.Container(
                    content=ft.Row([
                        ft.Text("Оголошення", size=17, weight=ft.FontWeight.BOLD, color=DARK),
                        self.count_text,
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.symmetric(horizontal=32, vertical=4),
                ),
                ft.Container(
                    content=self.car_list,
                    padding=ft.padding.symmetric(horizontal=32),
                    expand=True,
                ),
            ], expand=True, spacing=0)),
        )

        self.refresh_list()

    # ══════════════════════════════════════════════════════════════════════════
    # PICKER: Марка / Модель
    # ══════════════════════════════════════════════════════════════════════════
    def _init_brand_picker(self):
        self.brand_label  = ft.Text("Марка, Модель", size=14, color=GREY)
        self.brand_search = ft.TextField(
            label="Пошук марки", width=280, bgcolor=WHITE,
            border_color=LGREY, color=DARK, text_size=13,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
        )
        self.model_search = ft.TextField(
            label="Пошук моделі", width=280, bgcolor=WHITE,
            border_color=LGREY, color=DARK, text_size=13,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
        )
        self.brands_col = ft.Column(spacing=2, scroll=ft.ScrollMode.AUTO, height=150)
        self.models_col = ft.Column(spacing=2, scroll=ft.ScrollMode.AUTO, height=150)
        self._fill_brands()

        self.picker_panel = ft.Container(
            visible=False, bgcolor=WHITE, border_radius=12, padding=16, width=320,
            shadow=ft.BoxShadow(blur_radius=16, color="#25000000", offset=ft.Offset(0, 4)),
            content=ft.Column([
                self.brand_search, self.brands_col,
                self.model_search,
                ft.Text("ТОП моделі", size=12, weight=ft.FontWeight.W_600, color=DARK),
                self.models_col,
                ft.ElevatedButton("Застосувати", width=280,
                    style=ft.ButtonStyle(bgcolor=RED, color=WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.padding.symmetric(vertical=12)),
                    on_click=self._apply_picker),
            ], spacing=8, tight=True),
        )
        self.brand_search.on_change = lambda e: (
            self._fill_brands(self.brand_search.value or ""), self.page.update())
        self.model_search.on_change = lambda e: (
            self._fill_models(self.model_search.value or ""), self.page.update())

    def _make_brand_stack(self):
        t = _trigger(self.brand_label, self._toggle_picker)
        return ft.Stack([t, ft.Container(content=self.picker_panel,
                                          margin=ft.margin.only(top=48))], width=220)

    def _fill_brands(self, filter_text=""):
        self.brands_col.controls.clear()
        for brand in self._current_models.keys():
            if filter_text.lower() in brand.lower():
                self.brands_col.controls.append(
                    ft.TextButton(brand, style=ft.ButtonStyle(color=DARK),
                                  on_click=lambda e, b=brand: self._select_brand(b)))

    def _fill_models(self, filter_text=""):
        self.models_col.controls.clear()
        brand = self.selected_brand["v"]
        if not brand:
            return
        for model in self._current_models.get(brand, []):
            if filter_text.lower() in model.lower():
                self.models_col.controls.append(
                    ft.Checkbox(label=model, value=model in self.selected_models["v"],
                                active_color=RED,
                                on_change=lambda e, m=model: self._toggle_model(m, e.control.value)))

    def _select_brand(self, brand):
        self.selected_brand["v"] = brand
        self.selected_models["v"] = []
        self.brand_search.value = brand
        self._fill_models()
        self.page.update()

    def _toggle_model(self, model, checked):
        if checked and model not in self.selected_models["v"]:
            self.selected_models["v"].append(model)
        elif not checked and model in self.selected_models["v"]:
            self.selected_models["v"].remove(model)

    def _toggle_picker(self, e):
        type_map = {
            "Вантажівки": MODELS_TRUCKS,
            "Мотоцикли": MODELS_MOTORCYCLES,
            "Автобуси": MODELS_BUSES,
        }
        self._current_models = type_map.get(self.dd_type.value, MODELS)
        self._fill_brands()
        self.picker_panel.visible = not self.picker_panel.visible
        self.page.update()

    def _apply_picker(self, e):
        brand  = self.selected_brand["v"]
        models = self.selected_models["v"]
        self.brand_label.value = (f"{brand}, {', '.join(models)}" if brand and models
                                   else brand if brand else "Марка, Модель")
        self.picker_panel.visible = False
        self.page.update()

    # ══════════════════════════════════════════════════════════════════════════
    # PICKER: Рік випуску
    # ══════════════════════════════════════════════════════════════════════════
    def _init_year_picker(self):
        self.year_label    = ft.Text("Рік випуску", size=14, color=GREY)
        self.year_from_col = ft.Column(spacing=2, scroll=ft.ScrollMode.AUTO, height=200)
        self.year_to_col   = ft.Column(spacing=2, scroll=ft.ScrollMode.AUTO, height=200)
        self._fill_years()

        self.year_panel = ft.Container(
            visible=False, bgcolor=WHITE, border_radius=12, padding=16, width=320,
            shadow=ft.BoxShadow(blur_radius=16, color="#25000000", offset=ft.Offset(0, 4)),
            content=ft.Column([
                ft.Text("Рік випуску", size=14, weight=ft.FontWeight.W_600, color=DARK),
                ft.Row([
                    ft.Column([ft.Text("Від", size=13, weight=ft.FontWeight.W_600, color=DARK),
                               self.year_from_col], expand=True),
                    ft.VerticalDivider(width=1, color=LGREY),
                    ft.Column([ft.Text("До", size=13, weight=ft.FontWeight.W_600, color=DARK),
                               self.year_to_col], expand=True),
                ], spacing=12),
                ft.ElevatedButton("Застосувати", width=280,
                    style=ft.ButtonStyle(bgcolor=RED, color=WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.padding.symmetric(vertical=12)),
                    on_click=self._apply_year),
            ], spacing=10, tight=True),
        )

    def _make_year_stack(self):
        t = _trigger(self.year_label, self._toggle_year)
        return ft.Stack([t, ft.Container(content=self.year_panel,
                                          margin=ft.margin.only(top=48))], width=220)

    def _fill_years(self):
        years = [str(y) for y in range(2026, 1949, -1)]
        self.year_from_col.controls.clear()
        self.year_to_col.controls.clear()
        for y in years:
            self.year_from_col.controls.append(
                ft.TextButton(y, style=ft.ButtonStyle(color=DARK),
                              on_click=lambda e, yr=y: self._set_year("from", yr)))
            self.year_to_col.controls.append(
                ft.TextButton(y, style=ft.ButtonStyle(color=DARK),
                              on_click=lambda e, yr=y: self._set_year("to", yr)))

    def _set_year(self, side, year):
        if side == "from":
            self.year_from["v"] = year
        else:
            self.year_to["v"] = year
        self._update_year_label()
        self.page.update()

    def _update_year_label(self):
        yf, yt = self.year_from["v"], self.year_to["v"]
        if yf and yt:   self.year_label.value = f"{yf} — {yt}"
        elif yf:        self.year_label.value = f"Від {yf}"
        elif yt:        self.year_label.value = f"До {yt}"
        else:           self.year_label.value = "Рік випуску"

    def _toggle_year(self, e):
        self.year_panel.visible = not self.year_panel.visible
        self.page.update()

    def _apply_year(self, e):
        self._update_year_label()
        self.year_panel.visible = False
        self.page.update()

    # ══════════════════════════════════════════════════════════════════════════
    # PICKER: Вартість
    # ══════════════════════════════════════════════════════════════════════════
    def _init_price_picker(self):
        self.price_label = ft.Text("Вартість", size=14, color=GREY)
        self.tf_p_from = ft.TextField(
            label="Від $", width=250, bgcolor=WHITE, border_color=LGREY,
            color=DARK, text_size=13, keyboard_type=ft.KeyboardType.NUMBER,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        )
        self.tf_p_to = ft.TextField(
            label="До $", width=250, bgcolor=WHITE, border_color=LGREY,
            color=DARK, text_size=13, keyboard_type=ft.KeyboardType.NUMBER,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        )
        self.price_panel = ft.Container(
            visible=False, bgcolor=WHITE, border_radius=12, padding=16, width=300,
            shadow=ft.BoxShadow(blur_radius=16, color="#25000000", offset=ft.Offset(0, 4)),
            content=ft.Column([
                ft.Text("Вартість $", size=14, weight=ft.FontWeight.W_600, color=DARK),
                self.tf_p_from,
                self.tf_p_to,
                ft.ElevatedButton("Застосувати", width=250,
                    style=ft.ButtonStyle(bgcolor=RED, color=WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.padding.symmetric(vertical=12)),
                    on_click=self._apply_price),
            ], spacing=10, tight=True),
        )

    def _make_price_stack(self):
        t = _trigger(self.price_label, self._toggle_price)
        return ft.Stack([t, ft.Container(content=self.price_panel,
                                          margin=ft.margin.only(top=48))], width=220)

    def _toggle_price(self, e):
        self.price_panel.visible = not self.price_panel.visible
        self.page.update()

    def _apply_price(self, e):
        pf, pt = self.tf_p_from.value or "", self.tf_p_to.value or ""
        if pf and pt:   self.price_label.value = f"${pf} — ${pt}"
        elif pf:        self.price_label.value = f"Від ${pf}"
        elif pt:        self.price_label.value = f"До ${pt}"
        else:           self.price_label.value = "Вартість"
        self.price_panel.visible = False
        self.page.update()

    # ══════════════════════════════════════════════════════════════════════════
    # ПОШУК
    # ══════════════════════════════════════════════════════════════════════════
    def do_search(self, e=None):
        try:
            yf = int(self.year_from["v"]) if self.year_from["v"] else 0
            yt = int(self.year_to["v"])   if self.year_to["v"]   else 9999
            pf = float(self.tf_p_from.value.replace(",", ".")) if self.tf_p_from.value else 0
            pt = float(self.tf_p_to.value.replace(",", "."))   if self.tf_p_to.value   else float("inf")
        except ValueError:
            yf, yt, pf, pt = 0, 9999, 0, float("inf")

        cars = self.car_service.search_cars(
            brand=self.selected_brand["v"],
            model=self.selected_models["v"][0] if self.selected_models["v"] else "",
            year_from=yf, year_to=yt,
            price_from=pf, price_to=pt,
            fuel=self.dd_fuel.value or "",
            gearbox=self.dd_gear.value or "",
            region=self.dd_region.value or "",
            status="",
        )
        self.refresh_list(cars)

    def refresh_list(self, cars=None):
        if cars is None:
            cars = self.car_service.search_cars(status="")
        self.car_list.controls.clear()

        if not cars:
            self.car_list.controls.append(ft.Container(
                content=ft.Column([
                    ft.Text("🔍", size=42),
                    ft.Text("Нічого не знайдено", size=15, color=GREY),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                alignment=ft.Alignment.CENTER, padding=50,
            ))
        else:
            row = []
            for i, car in enumerate(cars):
                row.append(self._car_card(car))
                if len(row) == 3 or i == len(cars) - 1:
                    self.car_list.controls.append(ft.Row(row, spacing=14, wrap=True))
                    row = []

        self.count_text.value = f"Знайдено: {len(cars)} авт."
        self.page.update()

    def _car_card(self, car):
        sl = {"available": "Доступний", "sold": "Продано", "returned": "Повернено"}
        sc = {"available": "#27ae60", "sold": RED, "returned": "#f39c12"}

        # Фото або заглушка
        if getattr(car, "image", "") and car.image:
            photo = ft.Container(
                width=300, height=180,
                border_radius=ft.border_radius.only(top_left=10, top_right=10),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Image(src=car.image, width=300, height=180, fit="cover"),
            )
        else:
            photo = ft.Container(
                width=300, height=180, bgcolor="#e2e6f0",
                border_radius=ft.border_radius.only(top_left=10, top_right=10),
                content=ft.Column([
                    ft.Icon(ft.Icons.DIRECTIONS_CAR, size=52, color="#b0b8cc"),
                    ft.Text("Фото", size=12, color="#b0b8cc"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                   alignment=ft.MainAxisAlignment.CENTER),
            )

        return ft.Container(
            content=ft.Column([
                photo,
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"{car.brand} {car.model}", size=14,
                                    weight=ft.FontWeight.BOLD, color=DARK, expand=True),
                            ft.Container(
                                content=ft.Text(sl.get(car.status, ""), size=10,
                                                color=sc.get(car.status, GREY),
                                                weight=ft.FontWeight.W_600),
                                bgcolor="#f0f4f0", border_radius=20,
                                padding=ft.padding.symmetric(horizontal=8, vertical=3)),
                        ]),
                        ft.Text(f"📅 {car.year}   🚗 {car.mileage} тис.км", size=12, color=GREY),
                        ft.Text(f"⛽ {car.fuel or '—'}   🔧 {car.gearbox or '—'}", size=12, color=GREY),
                        ft.Text(f"📍 {car.city or car.region or '—'}", size=12, color=GREY),
                        ft.Divider(height=1, color=LGREY),
                        ft.Row([
                            ft.Text(f"${car.price:,.0f}", size=17,
                                    weight=ft.FontWeight.BOLD, color=RED, expand=True),
                            ft.Button("Деталі",
                                on_click=lambda e, c=car: self._show_detail(c),
                                style=ft.ButtonStyle(bgcolor=RED, color=WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=ft.padding.symmetric(horizontal=14, vertical=6))),
                        ]),
                    ], spacing=5),
                    padding=ft.padding.symmetric(horizontal=12, vertical=10),
                ),
            ], spacing=0),
            bgcolor=WHITE, border_radius=10, width=300,
            shadow=ft.BoxShadow(blur_radius=8, color="#18000000", offset=ft.Offset(0, 2)),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )


    def _show_detail(self, car):
        def close(e):
            dlg.open = False
            self.page.update()

        def buy(e):
            dlg.open = False
            self.page.update()

            tf_name  = ft.TextField(label="Ім'я", width=360, bgcolor=WHITE,
                                    border_color=LGREY, color=DARK, text_size=14,
                                    content_padding=ft.padding.symmetric(horizontal=12, vertical=10))
            tf_phone = ft.TextField(label="Телефон", width=360, bgcolor=WHITE,
                                    border_color=LGREY, color=DARK, text_size=14,
                                    keyboard_type=ft.KeyboardType.PHONE,
                                    content_padding=ft.padding.symmetric(horizontal=12, vertical=10))
            tf_email = ft.TextField(label="Email", width=360, bgcolor=WHITE,
                                    border_color=LGREY, color=DARK, text_size=14,
                                    keyboard_type=ft.KeyboardType.EMAIL,
                                    content_padding=ft.padding.symmetric(horizontal=12, vertical=10))
            err = ft.Text("", color=RED, size=13)

            def confirm_buy(e):
                if not tf_name.value or not tf_phone.value or not tf_email.value:
                    err.value = "Заповніть всі поля"
                    buy_dlg.update()
                    return

                self.order_service.add_order(
                    car_id=car.id,
                    car_brand=car.brand,
                    car_model=car.model,
                    car_price=car.price,
                    buyer_name=tf_name.value,
                    buyer_phone=tf_phone.value,
                    buyer_email=tf_email.value,
                )

                buy_dlg.open = False
                self.page.update()

                done = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("✅ Дякуємо за покупку!", size=17,
                                  weight=ft.FontWeight.BOLD, color=DARK),
                    content=ft.Text(
                        f"Ви придбали {car.brand} {car.model} за ${car.price:,.0f}.\n"
                        f"Наш менеджер зв'яжеться з вами найближчим часом.",
                        size=14, color=DARK,
                    ),
                    actions=[ft.TextButton("Закрити",
                        on_click=lambda e: (setattr(done, "open", False), self.page.update()))],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                self.page.overlay.append(done)
                done.open = True
                self.page.update()

            buy_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("🛒 Оформлення покупки", size=17,
                              weight=ft.FontWeight.BOLD, color=DARK),
                content=ft.Container(width=380, content=ft.Column([
                    ft.Text(f"{car.brand} {car.model}  •  ${car.price:,.0f}",
                            size=14, color=GREY),
                    ft.Divider(color=LGREY),
                    tf_name,
                    tf_phone,
                    tf_email,
                    err,
                ], spacing=12, tight=True)),
                actions=[
                    ft.TextButton("Скасувати",
                        on_click=lambda e: (setattr(buy_dlg, "open", False), self.page.update())),
                    ft.ElevatedButton(
                        "Підтвердити",
                        on_click=confirm_buy,
                        style=ft.ButtonStyle(
                            bgcolor=RED, color=WHITE,
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=20, vertical=10),
                            text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_600),
                        ),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.page.overlay.append(buy_dlg)
            buy_dlg.open = True
            self.page.update()

        # Фото у деталях або заглушка
        if getattr(car, "image", "") and car.image:
            detail_photo = ft.Container(
                width=400, height=220,
                border_radius=12,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Image(src=car.image, width=400, height=220, fit="cover"),
            )
        else:
            detail_photo = ft.Container(
                width=400, height=220, bgcolor="#e2e6f0", border_radius=12,
                content=ft.Column([
                    ft.Icon(ft.Icons.DIRECTIONS_CAR, size=64, color="#b0b8cc"),
                    ft.Text("Фото відсутнє", size=13, color="#b0b8cc"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                   alignment=ft.MainAxisAlignment.CENTER),
            )

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"{car.brand} {car.model}", size=18,
                          weight=ft.FontWeight.BOLD, color=DARK),
            content=ft.Container(width=400, content=ft.Column([
                detail_photo,
                ft.Container(height=4),
                ft.Row([
                    ft.Column([ft.Text("Рік", size=11, color=GREY),
                               ft.Text(str(car.year), size=14, weight=ft.FontWeight.W_600, color=DARK)]),
                    ft.Column([ft.Text("Ціна", size=11, color=GREY),
                               ft.Text(f"${car.price:,.0f}", size=14, weight=ft.FontWeight.W_600, color=RED)]),
                    ft.Column([ft.Text("Пробіг", size=11, color=GREY),
                               ft.Text(f"{car.mileage} тис.км", size=14, weight=ft.FontWeight.W_600, color=DARK)]),
                ], spacing=24),
                ft.Row([
                    ft.Column([ft.Text("Пальне", size=11, color=GREY),
                               ft.Text(car.fuel or "—", size=13, color=DARK)]),
                    ft.Column([ft.Text("Коробка", size=11, color=GREY),
                               ft.Text(car.gearbox or "—", size=13, color=DARK)]),
                    ft.Column([ft.Text("Кузов", size=11, color=GREY),
                               ft.Text(car.body_type or "—", size=13, color=DARK)]),
                ], spacing=24),
                ft.Row([
                    ft.Column([ft.Text("Регіон", size=11, color=GREY),
                               ft.Text(car.region or "—", size=13, color=DARK)]),
                    ft.Column([ft.Text("Місто", size=11, color=GREY),
                               ft.Text(car.city or "—", size=13, color=DARK)]),
                ], spacing=24),
            ], spacing=14, tight=True)),
            actions=[
                ft.TextButton("Закрити", on_click=close),
                ft.ElevatedButton(
                    "🛒  Купити",
                    on_click=buy,
                    style=ft.ButtonStyle(
                        bgcolor=RED, color=WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_600),
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()