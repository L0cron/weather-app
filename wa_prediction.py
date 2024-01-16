import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, NavigationDestination


def prediction()->list:
    return [
            AppBar(
                            title=Text("Прогнозирование"), bgcolor=colors.SURFACE_VARIANT,
                            actions = [
                                ElevatedButton(icon = ft.icons.KEYBOARD_RETURN_ROUNDED, text = 'Главное меню', color = ft.colors.BLACK, on_click = route_change),
                                ft.PopupMenuButton(
                                items=[
                                    ElevatedButton(icon = ft.icons.SETTINGS, text = 'Settings', color = ft.colors.BLACK, on_click=go_to_settings),
                                    ft.PopupMenuItem(),
                                    ElevatedButton(icon = ft.icons.KEYBOARD_RETURN, text = 'Return', color = ft.colors.BLACK, on_click = check_item_clicked),
                                ]
                            ),
                                ]
                               ),
            ]

