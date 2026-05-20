import flet as ft
from views.menu import MainView

def main(page: ft.Page):
    page.title = "AutoRIA — Система продажу автомобілів"
    state = {"user": None}

    def go(route):
        page.controls.clear()
        page.overlay.clear()

        if route == "/":
            view = MainView(page, on_sell=lambda: go("/login"))
            view.build()
        elif route == "/login":
            from views.login import LoginView
            view = LoginView(
                page,
                on_back=lambda: go("/"),
                on_success=lambda user: [state.update({"user": user}), go("/sell")]
            )
            view.build()
        elif route == "/sell":
            from views.sell import SellView
            view = SellView(page, user=state["user"], on_back=lambda: go("/"))
            view.build()

        page.update()

    go("/")

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)