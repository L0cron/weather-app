import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, NavigationDestination

import wa_options

def main(page: ft.Page):
    page.title = "Weather"

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

    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(
                        leading_width=40,
                        title=Text("Weather app"),
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
                    ft.NavigationBar(
                        destinations=[
                            NavigationDestination(icon=ft.icons.KEYBOARD_RETURN_ROUNDED, label="Главное меню"),
                            NavigationDestination(icon=ft.icons.BAR_CHART_ROUNDED, label="Анализ"),
                            NavigationDestination(icon=ft.icons.SHOW_CHART_ROUNDED, label="Визуализация"),
                            NavigationDestination(icon=ft.icons.WB_SUNNY_OUTLINED, label="Прогнозирование"),
                            NavigationDestination(icon=ft.icons.MONITOR, label="Мониторинг"),
                            NavigationDestination(icon=ft.icons.CLOUD_UPLOAD_OUTLINED, label="Загрузка файлов")
                        ]
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

#123
ft.app(target=main)