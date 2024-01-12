import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, NavigationDestination

def analyze()->list:
    return [
            AppBar(title=Text("Анализ"), bgcolor=colors.SURFACE_VARIANT),
            ElevatedButton(icon = ft.icons.WB_SUNNY_OUTLINED, text = 'Change theme', color = ft.colors.GREY),
            ]