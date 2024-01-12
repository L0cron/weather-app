import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, NavigationDestination, Container, IconButton

import wa_options
import wa_analyze

def main(page: ft.Page):
    page.title = "Weather"
    page.window_min_width = 1100
    page.window_min_height = 600

    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    def go_to_settings(e):
        page.go("/settings")
        page.views.append(
                View(
                    "/settings",
                    wa_options.settings(),
                )
            )
        page.update()

    def go_to_analyze(e):
        page.go("/analyze")
        page.views.append(
                View(
                    "/analyze",
                    wa_analyze.analyze(),
                )
            )
        page.update()

    



    def route_change(route):
        hgt = 75
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(
                        leading_width=40,
                        title=Text("Погода в г. Москва",color=ft.colors.PRIMARY, weight=ft.FontWeight.W_600),
                        center_title=False,
                        bgcolor=colors.SURFACE_VARIANT,
                        actions=[
                            ft.PopupMenuButton(
                                items=[
                                    ElevatedButton(icon = ft.icons.SETTINGS, text = 'Settings', color = ft.colors.BLACK, on_click=go_to_settings),
                                    ft.PopupMenuItem(),
                                    ElevatedButton(icon = ft.icons.KEYBOARD_RETURN, text = 'Return', color = ft.colors.BLACK, on_click = check_item_clicked),
                                ]   
                            ),
                        ],
                    ),
                    ft.BottomAppBar(
                        height=hgt,
                        padding=0,
                        content=ft.Row(controls=[
                            ft.ElevatedButton(icon=ft.icons.HOME_ROUNDED, text="Главное меню", style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=0)),expand=True,height=hgt,on_click=route_change),
                            ft.ElevatedButton(icon=ft.icons.BAR_CHART_ROUNDED, text="Анализ", style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=0)),expand=True,height=hgt,on_click=go_to_analyze),
                            ft.ElevatedButton(icon=ft.icons.SHOW_CHART_ROUNDED, text="Визуализация", style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=0)),expand=True,height=hgt),
                            ft.ElevatedButton(icon=ft.icons.WB_SUNNY_OUTLINED, text="Прогнозирование", style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=0)),expand=True,height=hgt),
                            ft.ElevatedButton(icon=ft.icons.MONITOR, text="Мониторинг", style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=0)),expand=True,height=hgt),
                            ft.ElevatedButton(icon=ft.icons.CLOUD_UPLOAD_OUTLINED, text="Загрузка файлов", style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=0)),expand=True,height=hgt),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        )
                    ),
                ],
            )
        )
        
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)