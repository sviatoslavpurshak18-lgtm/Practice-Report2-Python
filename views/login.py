import flet as ft
import re
from services.customer_service import CustomerService
from models.customer import Customer

RED   = "#e8192c"
WHITE = "#ffffff"
BG    = "#f0f2f5"
DARK  = "#1a1a2e"
GREY  = "#8a8fa8"
LGREY = "#d4d8e6"


class LoginView:
    def __init__(self, page: ft.Page, on_back=None, on_success=None):
        self.page = page
        self.on_back = on_back
        self.on_success = on_success
        self.svc = CustomerService()
        self.mode = "login"

    def build(self):
        self.page.clean()
        self.page.bgcolor = BG

        self.tf_name  = ft.TextField(label="Ім'я або Нік-нейм", width=340,
                                      bgcolor=WHITE, border_color=LGREY,
                                      focused_border_color=RED, color=DARK)
        self.tf_email = ft.TextField(label="Email", width=340,
                                      bgcolor=WHITE, border_color=LGREY,
                                      focused_border_color=RED, color=DARK)
        self.tf_pass  = ft.TextField(label="Пароль", password=True,
                                      can_reveal_password=True, width=340,
                                      bgcolor=WHITE, border_color=LGREY,
                                      focused_border_color=RED, color=DARK)
        self.tf_pass2 = ft.TextField(label="Підтвердіть пароль", password=True,
                                      can_reveal_password=True, width=340,
                                      bgcolor=WHITE, border_color=LGREY,
                                      focused_border_color=RED, color=DARK)

        self.name_row  = ft.Column([self.tf_name],  visible=False)
        self.pass2_row = ft.Column([self.tf_pass2], visible=False)

        self.title      = ft.Text("Увійти в акаунт", size=22,
                                   weight=ft.FontWeight.BOLD, color=DARK)
        self.err_text   = ft.Text("", color=RED, size=13)
        self.hint_lbl   = ft.Text("Ще немає акаунту? ", size=13, color=GREY)
        self.switch_btn = ft.TextButton("Зареєструватись",
                                         style=ft.ButtonStyle(color=RED),
                                         on_click=self.toggle)
        self.submit_btn = ft.Button(
            "Увійти", width=340,
            style=ft.ButtonStyle(
                bgcolor=RED, color=WHITE,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.padding.symmetric(vertical=14),
                text_style=ft.TextStyle(size=15, weight=ft.FontWeight.W_600),
            ),
            on_click=self.do_submit,
        )

        card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.IconButton(ft.Icons.ARROW_BACK, icon_color=DARK,
                                  on_click=lambda e: self.on_back() if self.on_back else None),
                    ft.Container(expand=True),
                ]),
                ft.Row([
                    ft.Container(content=ft.Text("auto", size=17,
                                                  weight=ft.FontWeight.BOLD, color=WHITE),
                                 bgcolor=RED, border_radius=4,
                                 padding=ft.padding.symmetric(horizontal=8, vertical=3)),
                    ft.Container(content=ft.Text("UA", size=17,
                                                  weight=ft.FontWeight.BOLD, color=WHITE),
                                 bgcolor="#003580", border_radius=4,
                                 padding=ft.padding.symmetric(horizontal=8, vertical=3)),
                ], spacing=2),
                ft.Container(height=6),
                self.title,
                ft.Text("Увійдіть або зареєструйтесь щоб розмістити оголошення",
                        size=13, color=GREY, text_align=ft.TextAlign.CENTER),
                ft.Container(height=4),
                self.name_row,
                self.tf_email,
                self.tf_pass,
                self.pass2_row,
                self.err_text,
                ft.Container(height=4),
                self.submit_btn,
                ft.Row([self.hint_lbl, self.switch_btn], spacing=0,
                       alignment=ft.MainAxisAlignment.CENTER),
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
               tight=True),
            bgcolor=WHITE, border_radius=20, padding=32, width=420,
            shadow=ft.BoxShadow(blur_radius=24, color="#20000000",
                                offset=ft.Offset(0, 8)),
        )

        self.page.add(
            ft.Container(
                content=card,
                alignment=ft.Alignment.CENTER,
                expand=True,
                bgcolor=BG,
            )
        )

    def toggle(self, e=None):
        self.err_text.value = ""
        self.err_text.color = RED
        if self.mode == "login":
            self.mode = "register"
            self.title.value       = "Реєстрація продавця"
            self.hint_lbl.value    = "Вже маєте акаунт? "
            self.switch_btn.text   = "Увійти"
            self.submit_btn.text   = "Зареєструватись"
            self.name_row.visible  = True
            self.pass2_row.visible = True
        else:
            self.mode = "login"
            self.title.value       = "Увійти в акаунт"
            self.hint_lbl.value    = "Ще немає акаунту? "
            self.switch_btn.text   = "Зареєструватись"
            self.submit_btn.text   = "Увійти"
            self.name_row.visible  = False
            self.pass2_row.visible = False
        self.submit_btn.update()
        self.page.update()

    def do_submit(self, e):
        self.err_text.value = ""
        self.err_text.color = RED
        email = (self.tf_email.value or "").strip()
        pwd   = self.tf_pass.value or ""

        pattern = r"^[\w\.\-]+@[\w\.\-]+\.\w{2,}$"
        if not re.match(pattern, email):
            self.err_text.value = "Невірний пароль або email"
            self.page.update()
            return

        if not email or not pwd:
            self.err_text.value = "Заповніть всі поля"
            self.page.update()
            return

        if self.mode == "login":
            customer, msg = self.svc.login(email, pwd)
            if customer:
                if self.on_success:
                    self.on_success(customer)
            else:
                self.err_text.value = msg
                self.page.update()
        else:
            name = (self.tf_name.value or "").strip()
            if not name:
                self.err_text.value = "Введіть ім'я"
                self.page.update()
                return
            if pwd != (self.tf_pass2.value or ""):
                self.err_text.value = "Паролі не збігаються"
                self.page.update()
                return
            if len(pwd) < 4:
                self.err_text.value = "Пароль мінімум 4 символи"
                self.page.update()
                return

            ok, msg = self.svc.register_customer(
                Customer(id=0, name=name, email=email, password=pwd))

            if ok:
                self.err_text.color = "#27ae60"
                self.err_text.value = "Реєстрація успішна! Тепер увійдіть."
                self.page.update()
                self.toggle()
            else:
                self.err_text.value = msg
                self.page.update()