
import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, NavigationDestination, Container, IconButton

page:ft.Page = None

import wa_options
import wa_analyze
import wa_prediction

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


def go_to_prediction(e):
    page.go("/prediction")
    page.views.append(
            View(
                "/prediction",
                wa_prediction.prediction(),
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


def route_change(pg, route):
    global page
    page = pg

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
                        ft.ElevatedButton(icon=ft.icons.WB_SUNNY_OUTLINED, text="Прогнозирование", style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=0)),expand=True,height=hgt, on_click = go_to_prediction),
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