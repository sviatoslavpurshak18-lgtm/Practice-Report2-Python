import flet as ft
from services.car_service import CarService

RED   = "#e8192c"
WHITE = "#ffffff"
BG    = "#f0f2f5"
DARK  = "#1a1a2e"
GREY  = "#8a8fa8"
LGREY = "#d4d8e6"

MODELS = {
    "BMW": ["1 Series","2 Series","3 Series","4 Series","5 Series","6 Series",
            "7 Series","8 Series","X1","X2","X3","X4","X5","X6","X7",
            "Z4","M2","M3","M4","M5","M8","i3","i4","i7","i8","XM"],
    "Mercedes-Benz": ["A-Class","B-Class","C-Class","CLA","CLS","E-Class",
                      "S-Class","GLA","GLB","GLC","GLE","GLS","G-Class",
                      "AMG GT","EQC","EQS","SL","V-Class"],
    "Audi": ["A1","A3","A4","A5","A6","A7","A8",
             "Q2","Q3","Q5","Q7","Q8",
             "TT","R8","RS3","RS4","RS5","RS6","RS7","e-tron"],
    "Toyota": ["Aygo","Yaris","Corolla","Camry","Avalon","Prius",
               "C-HR","RAV4","Highlander","Land Cruiser","Hilux",
               "Supra","Tacoma","Tundra","Sequoia"],
    "Volkswagen": ["Polo","Golf","Jetta","Passat","Arteon",
                   "T-Cross","T-Roc","Tiguan","Touareg","Atlas",
                   "Beetle","Scirocco","ID.3","ID.4"],
    "Honda": ["Jazz","Civic","Accord","Insight","CR-V","HR-V",
              "Pilot","Ridgeline","Passport","Odyssey","e"],
    "Hyundai": ["i10","i20","i30","Elantra","Sonata","Accent",
                "Tucson","Santa Fe","Palisade","Kona","Creta",
                "Veloster","Ioniq","IONIQ 5"],
    "Kia": ["Picanto","Rio","Ceed","Cerato","K5","Stinger",
            "Sportage","Sorento","Telluride","Soul","Niro",
            "Seltos","EV6"],
    "Ford": ["Fiesta","Focus","Mondeo","Fusion","Mustang",
             "Explorer","Escape","Edge","Kuga","Bronco",
             "Ranger","F-150","Maverick"],
    "Chevrolet": ["Spark","Aveo","Cruze","Malibu","Impala",
                  "Camaro","Corvette","Trailblazer","Equinox",
                  "Traverse","Tahoe","Suburban","Silverado"],
    "Mazda": ["Mazda2","Mazda3","Mazda6","CX-3","CX-30",
              "CX-5","CX-7","CX-9","MX-5","RX-8"],
    "Skoda": ["Fabia","Scala","Rapid","Octavia","Superb",
              "Kamiq","Karoq","Kodiaq","Enyaq"],
    "Renault": ["Clio","Megane","Logan","Sandero","Talisman",
                "Captur","Kadjar","Koleos","Duster","Scenic","Arkana"],
    "Opel": ["Corsa","Astra","Vectra","Insignia","Mokka",
             "Crossland","Grandland","Zafira"],
    "Nissan": ["Micra","Note","Sentra","Altima","Maxima",
               "Juke","Qashqai","X-Trail","Murano","Pathfinder",
               "Patrol","Leaf","370Z","GT-R","Navara"],
    "Porsche": ["911","Panamera","Cayenne","Macan","Taycan","718 Boxster","718 Cayman"],
    "Lexus": ["IS","ES","GS","LS","UX","NX","RX","GX","LX","LC"],
    "Tesla": ["Model S","Model 3","Model X","Model Y","Cybertruck","Roadster"],
    "Subaru": ["Impreza","Legacy","WRX","Forester","Outback","XV","BRZ"],
    "Peugeot": ["208","308","508","2008","3008","5008","Rifter"],
    "Volvo": ["S60","S90","V60","V90","XC40","XC60","XC90","C40"],
    "Jeep": ["Renegade","Compass","Cherokee","Grand Cherokee","Wrangler","Gladiator"],
    "Ferrari": ["488","F8","Roma","Portofino","SF90 Stradale","812 Superfast"],
    "Lamborghini": ["Huracan","Aventador","Urus","Revuelto"],
    "Bentley": ["Continental GT","Flying Spur","Bentayga"],
    "Rolls-Royce": ["Ghost","Phantom","Cullinan","Wraith"],
    "Bugatti": ["Veyron","Chiron","Divo","Bolide"]
}
MODELS_TRUCKS = {
    "Mercedes-Benz Trucks": ["Actros","Atego","Arocs","Axor","Econic",
                             "Unimog","Zetros","Sprinter","Vario"],

    "MAN": ["TGX","TGS","TGM","TGL","Lion's Coach",
            "Lion's City","F2000","TGA"],

    "Volvo Trucks": ["FH","FH16","FM","FMX","FL","FE",
                     "VNL","VNR","VHD"],

    "Scania": ["R Series","S Series","G Series","P Series",
               "L Series","XT","Touring"],

    "DAF": ["XF","XG","XG+","CF","LF"],

    "Iveco": ["Stralis","S-Way","X-Way","Eurocargo",
              "Daily","Trakker"],

    "Renault Trucks": ["T Series","T High","C Series",
                       "K Series","D Series","Master"],

    "КАМАЗ": ["4310","43118","4350","5350","5490",
              "55111","6520","65115","6560"],

    "ГАЗ": ["Газель Next","Газель Business","Газон Next",
            "Соболь","Валдай","Садко Next"],

    "Богдан": ["A-069","A-092","A-144","E-1","E701"],

    "Ford Trucks": ["F-MAX","Cargo","Transit","F-Line"],

    "Mack": ["Anthem","Pinnacle","Granite","LR","TerraPro"],

    "Kenworth": ["T680","T880","W900","K270","K370"],

    "Peterbilt": ["579","567","389","520","535"],

    "Freightliner": ["Cascadia","M2 106","122SD","114SD","eCascadia"],

    "Western Star": ["4700","4900","5700XE","49X"],

    "Isuzu": ["N-Series","F-Series","Giga","Forward"],

    "Hino": ["300 Series","500 Series","700 Series","Profia"],

    "Tatra": ["Phoenix","Force","T815","TerrNo1"],

    "Ural": ["4320","5557","6370","Next"],

    "MAZ": ["4370","5336","5440","6312","6501"],

    "FAW": ["J6","J7","Tiger V","CA3250"],

    "Sinotruk": ["HOWO","Sitrak","Steyr King","Hohan"],

    "Dongfeng": ["KL","KR","Captain","T-Lift"],

    "Shacman": ["X3000","F3000","M3000"],

    "Tesla Semi": ["Semi"],

    "Nikola": ["Tre","Two"],

    "BMC": ["Pro 827","Tugra","Professional"]
}
BRANDS  = list(MODELS.keys())
FUELS   = ["Бензин","Дизель","Електро","Гібрид","Газ"]
GEARS   = ["Автомат","Механіка","Робот","Варіатор"]
REGIONS = ["Київська", "Харківська", "Львівська", "Одеська", "Дніпропетровська",
           "Запорізька", "Полтавська", "Вінницька", "Черкаська", "Тернопільська",
           "Волинська", "Донецька", "Житомирська", "Закарпатська",
           "Івано-Франківська", "Кіровоградська", "Луганська", "Миколаївська",
           "Рівненська", "Сумська", "Херсонська", "Хмельницька",
           "Чернівецька", "Чернігівська", "Крим"]
TYPES   = ["Легкові","Вантажівки"]


class MainView:
    def __init__(self, page: ft.Page, on_sell=None, on_logout=None, current_user=None):
        self.page = page
        self.car_service = CarService()
        self.on_sell = on_sell
        self.on_logout = on_logout
        self.current_user = current_user
        self.page.title = "AutoRIA — Система продажу автомобілів"
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
            bgcolor=WHITE, border_color=LGREY, color=DARK,
        )
        self.dd_fuel = ft.Dropdown(
            label="Пальне", width=200,
            options=[ft.dropdown.Option(f) for f in FUELS],
            bgcolor=WHITE, border_color=LGREY, color=DARK,
        )
        self.dd_gear = ft.Dropdown(
            label="Коробка передач", width=200,
            options=[ft.dropdown.Option(g) for g in GEARS],
            bgcolor=WHITE, border_color=LGREY, color=DARK,
        )
        self.dd_region = ft.Dropdown(
            label="Регіон", width=200,
            options=[ft.dropdown.Option(r) for r in REGIONS],
            bgcolor=WHITE, border_color=LGREY, color=DARK,
        )
        self.tf_price_from = ft.TextField(
            label="Ціна від $", width=130,
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor=WHITE, border_color=LGREY, color=DARK,
        )
        self.tf_price_to = ft.TextField(
            label="Ціна до $", width=130,
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor=WHITE, border_color=LGREY, color=DARK,
        )

        brand_model_picker = self._build_brand_model_picker()
        year_picker        = self._build_year_picker()

        filters_block = ft.Container(
            content=ft.Column([
                ft.Text("Знаємо, бо перевірили", size=26,
                        weight=ft.FontWeight.BOLD, color=DARK),
                ft.Row([
                    self.dd_type,
                    brand_model_picker,
                    year_picker,
                    ft.Row([self.tf_price_from,
                            ft.Text("—", color=GREY),
                            self.tf_price_to], spacing=4),
                ], spacing=12, wrap=True),
                ft.Row([
                    self.dd_region,
                    self.dd_fuel,
                    self.dd_gear,
                ], spacing=12),
                ft.ElevatedButton(
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
                        content=ft.Text("auto", size=17,
                                        weight=ft.FontWeight.BOLD, color=WHITE),
                        bgcolor=RED, border_radius=4,
                        padding=ft.padding.symmetric(horizontal=8, vertical=3)),
                    ft.Container(
                        content=ft.Text("RIA", size=17,
                                        weight=ft.FontWeight.BOLD, color=WHITE),
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
                        ft.Text("Оголошення", size=17,
                                weight=ft.FontWeight.BOLD, color=DARK),
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

    # ── Picker Марка/Модель ────────────────────────────────────────────────────
    def _build_brand_model_picker(self):
        self.brand_label  = ft.Text("Марка, Модель", size=13, color=GREY)
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
                self.brand_search,
                self.brands_col,
                self.model_search,
                ft.Text("ТОП моделі", size=12, weight=ft.FontWeight.W_600, color=DARK),
                self.models_col,
                ft.ElevatedButton(
                    "Застосувати", width=280,
                    style=ft.ButtonStyle(
                        bgcolor=RED, color=WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.padding.symmetric(vertical=12),
                    ),
                    on_click=self._apply_picker,
                ),
            ], spacing=8, tight=True),
        )

        self.brand_search.on_change = lambda e: (
            self._fill_brands(self.brand_search.value or ""), self.page.update())
        self.model_search.on_change = lambda e: (
            self._fill_models(self.model_search.value or ""), self.page.update())

        trigger = ft.Container(
            content=ft.Row([
                self.brand_label,
                ft.Container(expand=True),
                ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=GREY, size=18),
            ]),
            bgcolor=WHITE, border_radius=8,
            border=ft.border.all(1, LGREY),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            width=220, on_click=self._toggle_picker,
        )

        return ft.Column([trigger, self.picker_panel], spacing=4)

    def _fill_brands(self, filter_text=""):
        self.brands_col.controls.clear()
        for brand in self._current_models.keys():
            if filter_text.lower() in brand.lower():
                self.brands_col.controls.append(
                    ft.TextButton(brand, style=ft.ButtonStyle(color=DARK),
                                  on_click=lambda e, b=brand: self._select_brand(b))
                )

    def _fill_models(self, filter_text=""):
        self.models_col.controls.clear()
        brand = self.selected_brand["v"]
        if not brand:
            return
        for model in self._current_models.get(brand, []):
            if filter_text.lower() in model.lower():
                self.models_col.controls.append(
                    ft.Checkbox(label=model,
                                value=model in self.selected_models["v"],
                                active_color=RED,
                                on_change=lambda e, m=model: self._toggle_model(m, e.control.value))
                )

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
        self._current_models = MODELS_TRUCKS if self.dd_type.value == "Вантажівки" else MODELS
        self._fill_brands()
        self.picker_panel.visible = not self.picker_panel.visible
        self.page.update()

    def _apply_picker(self, e):
        brand  = self.selected_brand["v"]
        models = self.selected_models["v"]
        if brand and models:
            self.brand_label.value = f"{brand}, {', '.join(models)}"
        elif brand:
            self.brand_label.value = brand
        else:
            self.brand_label.value = "Марка, Модель"
        self.picker_panel.visible = False
        self.page.update()

    # ── Picker Рік випуску ─────────────────────────────────────────────────────
    def _build_year_picker(self):
        self.year_label    = ft.Text("Рік випуску", size=13, color=GREY)
        self.year_from_col = ft.Column(spacing=2, scroll=ft.ScrollMode.AUTO, height=200)
        self.year_to_col   = ft.Column(spacing=2, scroll=ft.ScrollMode.AUTO, height=200)

        self._fill_years()

        self.year_panel = ft.Container(
            visible=False, bgcolor=WHITE, border_radius=12, padding=16, width=320,
            shadow=ft.BoxShadow(blur_radius=16, color="#25000000", offset=ft.Offset(0, 4)),
            content=ft.Column([
                ft.Text("Рік випуску", size=14, weight=ft.FontWeight.W_600, color=DARK),
                ft.Row([
                    ft.Column([
                        ft.Text("Від", size=13, weight=ft.FontWeight.W_600, color=DARK),
                        self.year_from_col,
                    ], expand=True),
                    ft.VerticalDivider(width=1, color=LGREY),
                    ft.Column([
                        ft.Text("До", size=13, weight=ft.FontWeight.W_600, color=DARK),
                        self.year_to_col,
                    ], expand=True),
                ], spacing=12),
                ft.ElevatedButton(
                    "Застосувати", width=280,
                    style=ft.ButtonStyle(
                        bgcolor=RED, color=WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.padding.symmetric(vertical=12),
                    ),
                    on_click=self._apply_year,
                ),
            ], spacing=10, tight=True),
        )

        trigger = ft.Container(
            content=ft.Row([
                self.year_label,
                ft.Container(expand=True),
                ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=GREY, size=18),
            ]),
            bgcolor=WHITE, border_radius=8,
            border=ft.border.all(1, LGREY),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            width=220, on_click=self._toggle_year,
        )

        return ft.Column([trigger, self.year_panel], spacing=4)

    def _fill_years(self):
        years = [str(y) for y in range(2026, 1989, -1)]
        self.year_from_col.controls.clear()
        self.year_to_col.controls.clear()
        for y in years:
            self.year_from_col.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Radio(value=y, fill_color=RED),
                        ft.Text(y, size=13, color=DARK),
                    ], spacing=4),
                    on_click=lambda e, yr=y: self._set_year("from", yr),
                )
            )
            self.year_to_col.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Radio(value=y, fill_color=RED),
                        ft.Text(y, size=13, color=DARK),
                    ], spacing=4),
                    on_click=lambda e, yr=y: self._set_year("to", yr),
                )
            )

    def _set_year(self, side, year):
        if side == "from":
            self.year_from["v"] = year
        else:
            self.year_to["v"] = year
        self._update_year_label()
        self.page.update()

    def _update_year_label(self):
        yf = self.year_from["v"]
        yt = self.year_to["v"]
        if yf and yt:
            self.year_label.value = f"{yf} — {yt}"
        elif yf:
            self.year_label.value = f"Від {yf}"
        elif yt:
            self.year_label.value = f"До {yt}"
        else:
            self.year_label.value = "Рік випуску"

    def _toggle_year(self, e):
        self.year_panel.visible = not self.year_panel.visible
        self.page.update()

    def _apply_year(self, e):
        self._update_year_label()
        self.year_panel.visible = False
        self.page.update()

    # ── Пошук ─────────────────────────────────────────────────────────────────
    def do_search(self, e=None):
        try:
            yf = int(self.year_from["v"]) if self.year_from["v"] else 0
            yt = int(self.year_to["v"])   if self.year_to["v"]   else 9999
            pf = float(self.tf_price_from.value.replace(",", ".")) if self.tf_price_from.value else 0
            pt = float(self.tf_price_to.value.replace(",", "."))   if self.tf_price_to.value   else float("inf")
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
                            ft.ElevatedButton(
                                "Деталі",
                                on_click=lambda e, c=car: self._show_detail(c),
                                style=ft.ButtonStyle(
                                    bgcolor=RED, color=WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=ft.padding.symmetric(horizontal=14, vertical=6)),
                            ),
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

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"{car.brand} {car.model}", size=18,
                          weight=ft.FontWeight.BOLD, color=DARK),
            content=ft.Container(width=400, content=ft.Column([
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
            actions=[ft.TextButton("Закрити", on_click=close)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()