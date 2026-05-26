import flet as ft
import base64
from services.car_service import CarService

RED   = "#e8192c"
WHITE = "#ffffff"
BG    = "#f0f2f5"
DARK  = "#1a1a2e"
GREY  = "#8a8fa8"
LGREY = "#d4d8e6"
FUELS = ["Бензин", "Дизель", "Електро", "Гібрид", "Газ", "Бензин + Газ (ГБО)",
         "Плагін-гібрид", "Водень", "Біопаливо", "Метан", "Пропан", "Етанол"]
GEARS      = ["Автомат","Механіка","Робот","Варіатор"]
YEARS      = [str(y) for y in range(2025, 1949, -1)]
REGIONS = [
    "Вінницька", "Волинська", "Дніпропетровська", "Житомирська",
    "Закарпатська", "Івано-Франківська", "Київська", "Кіровоградська",
    "Львівська", "Миколаївська", "Одеська", "Полтавська",
    "Рівненська", "Сумська", "Тернопільська", "Харківська",
    "Хмельницька", "Черкаська", "Чернівецька", "Чернігівська"
]
CITIES = [
    "Вінниця", "Луцьк", "Дніпро", "Житомир", "Ужгород",
    "Івано-Франківськ", "Київ", "Кропивницький", "Львів",
    "Миколаїв", "Одеса", "Полтава", "Рівне", "Суми",
    "Тернопіль", "Харків", "Хмельницький", "Черкаси",
    "Чернівці", "Чернігів"
]
TYPES = ["Легкові", "Вантажівки", "Мотоцикли", "Автобуси"]
W = 500


def _dd(options, width=W):
    return ft.Dropdown(
        hint_text="Оберіть",
        options=[ft.dropdown.Option(o) for o in options],
        width=width, bgcolor=WHITE, border_color=LGREY,
        border_radius=8, color=DARK,
        hint_style=ft.TextStyle(color=GREY, size=14),
        content_padding=ft.padding.symmetric(horizontal=14, vertical=10),
        text_size=14,
    )


def _tf(hint, width=W):
    return ft.TextField(
        hint_text=hint, width=width, bgcolor=WHITE,
        border_color=LGREY, border_radius=8, color=DARK,
        hint_style=ft.TextStyle(color=GREY, size=14),
        content_padding=ft.padding.symmetric(horizontal=14, vertical=10),
        text_size=14,
    )


def _row(label, control, required=True):
    return ft.Row([
        ft.Container(
            content=ft.Row([
                ft.Text(label, size=14, color=DARK),
                ft.Text(" *", color=RED, size=14) if required else ft.Container(),
            ], spacing=2),
            width=180,
        ),
        control,
    ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER)


class SellView:
    def __init__(self, page: ft.Page, user=None, on_back=None):
        self.page       = page
        self.user       = user
        self.on_back    = on_back
        self.svc        = CarService()
        self.image_path = {"v": ""}

    def build(self):
        self.page.clean()
        self.page.bgcolor = BG

        self.dd_type   = _dd(TYPES)
        self.tf_brand  = _tf("Введіть марку авто")
        self.tf_model  = _tf("Введіть модель авто")
        self.dd_year   = _dd(YEARS, width=200)
        self.dd_fuel   = _dd(FUELS)
        self.dd_gear   = _dd(GEARS)
        self.dd_region = _dd(REGIONS)
        self.dd_city   = _dd(CITIES)
        self.tf_miles  = _tf("тис.км", width=200)
        self.tf_mod    = _tf("Модифікація (необов'язково)")
        self.tf_price  = _tf("Введіть ціну в $")
        self.err_text  = ft.Text("", color=RED, size=13)

        # ── Фото блок ──────────────────────────────────────────────────────────
        self.photo_name = ft.Text("Файл не обрано", size=12, color=GREY)
        self.photo_preview = ft.Container(
            width=280, height=180,
            bgcolor="#e8eaf0",
            border_radius=12,
            content=ft.Column([
                ft.Icon(ft.Icons.ADD_PHOTO_ALTERNATE, size=48, color=GREY),
                ft.Text("Натисніть щоб обрати фото", size=12, color=GREY,
                        text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
               alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        )

        async def pick_image_file(e):
            files = await ft.FilePicker().pick_files(
                dialog_title="Оберіть фото автомобіля",
                file_type=ft.FilePickerFileType.IMAGE,
                with_data=True,
            )
            if not files:
                self.photo_name.value = "Вибір скасовано"
            else:
                f = files[0]
                self.photo_name.value = f.name
                ext  = f.name.split(".")[-1].lower()
                mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
                        "png": "image/png",  "webp": "image/webp"}.get(ext, "image/jpeg")
                b64 = base64.b64encode(f.bytes).decode("utf-8")
                data_url = f"data:{mime};base64,{b64}"
                self.photo_preview.content = ft.Image(
                    src=data_url, width=280, height=180,
                    fit=ft.BoxFit.COVER, border_radius=12)
                self.image_path["v"] = data_url
            self.page.update()

        photo_block = ft.Container(
            content=ft.Column([
                ft.Divider(color=LGREY),
                ft.Text("Фото автомобіля", size=16,
                        weight=ft.FontWeight.BOLD, color=DARK),
                ft.Text("Додайте фото щоб оголошення помітили швидше",
                        size=12, color=GREY),
                ft.Container(height=4),
                ft.Row([
                    self.photo_preview,
                    ft.Column([
                        ft.Button(
                            "📁  Обрати фото", width=220,
                            style=ft.ButtonStyle(
                                bgcolor="#f0f4ff", color=DARK,
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=ft.padding.symmetric(vertical=12),
                                text_style=ft.TextStyle(size=14),
                            ),
                            on_click=pick_image_file,
                        ),
                        self.photo_name,
                    ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                ], spacing=20, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ], spacing=8),
        )

        # ── Navbar ─────────────────────────────────────────────────────────────
        navbar = ft.Container(
            content=ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, icon_color=DARK,
                              on_click=lambda e: self.on_back() if self.on_back else None),
                ft.Row([
                    ft.Container(
                        content=ft.Text("auto", size=17,
                                        weight=ft.FontWeight.BOLD, color=WHITE),
                        bgcolor=RED, border_radius=4,
                        padding=ft.padding.symmetric(horizontal=8, vertical=3)),
                    ft.Container(
                        content=ft.Text("UA", size=17,
                                        weight=ft.FontWeight.BOLD, color=WHITE),
                        bgcolor="#003580", border_radius=4,
                        padding=ft.padding.symmetric(horizontal=8, vertical=3)),
                ], spacing=2),
                ft.Text("Розмістити оголошення", size=15,
                        weight=ft.FontWeight.BOLD, color=DARK),
                ft.Container(expand=True),
                ft.Text(f"👤 {self.user.name}" if self.user else "",
                        size=13, color=GREY),
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=WHITE,
            padding=ft.padding.symmetric(horizontal=24, vertical=12),
            shadow=ft.BoxShadow(blur_radius=6, color="#10000000", offset=ft.Offset(0, 2)),
        )

        # ── Форма ──────────────────────────────────────────────────────────────
        form = ft.Container(
            content=ft.Column([
                ft.Text("Додати оголошення", size=20,
                        weight=ft.FontWeight.BOLD, color=DARK),
                ft.Divider(color=LGREY),
                _row("Тип транспорту",  self.dd_type),
                _row("Марка авто",      self.tf_brand),
                _row("Модель авто",     self.tf_model),
                _row("Рік випуску",     self.dd_year),
                _row("Пробіг",          self.tf_miles,  required=False),
                _row("Модифікація",     self.tf_mod,    required=False),
                _row("Регіон",          self.dd_region),
                _row("Місто",           self.dd_city),
                _row("Пальне",          self.dd_fuel,   required=False),
                _row("Коробка передач", self.dd_gear,   required=False),
                _row("Ціна $",          self.tf_price),
                # ── Фото знизу форми ──────────────────────────────────────────
                photo_block,
                self.err_text,
                ft.Container(height=8),
                ft.Button(
                    "📤  Опублікувати оголошення", width=700,
                    style=ft.ButtonStyle(
                        bgcolor=RED, color=WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.padding.symmetric(vertical=14),
                        text_style=ft.TextStyle(size=15, weight=ft.FontWeight.W_600),
                    ),
                    on_click=self.submit,
                ),
            ], spacing=14, scroll=ft.ScrollMode.AUTO),
            bgcolor=WHITE, border_radius=16, padding=32,
            shadow=ft.BoxShadow(blur_radius=12, color="#12000000", offset=ft.Offset(0, 4)),
            expand=True,
        )

        self.page.add(
            navbar,
            ft.Container(
                content=form,
                expand=True,
                bgcolor=BG,
                padding=ft.padding.all(32),
            )
        )

    def submit(self, e):
        required = [
            (self.dd_type,   "Тип транспорту"),
            (self.tf_brand,  "Марка"),
            (self.tf_model,  "Модель"),
            (self.dd_year,   "Рік"),
            (self.dd_region, "Регіон"),
            (self.dd_city,   "Місто"),
            (self.tf_price,  "Ціна"),
        ]
        missing = [n for f, n in required if not f.value]
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
            brand=self.tf_brand.value,
            model=self.tf_model.value,
            price=price,
            year=int(self.dd_year.value),
            region=self.dd_region.value,
            fuel=self.dd_fuel.value or "",
            gearbox=self.dd_gear.value or "",
            mileage=miles,
            city=self.dd_city.value or "",
            image=self.image_path["v"],
        )

        self.err_text.color = "#27ae60"
        self.err_text.value = "✅ Оголошення успішно розміщено!"
        self.page.update()