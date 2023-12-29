import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, NavigationDestination

def settings()->list:
    return [
            AppBar(title=Text("Settings"), bgcolor=colors.BLACK),
            ElevatedButton(icon = ft.icons.WB_SUNNY_OUTLINED, text = 'Change theme', color = ft.colors.WHITE),
            ]