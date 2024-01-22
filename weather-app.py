import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, NavigationDestination



import wa_routes

def main(page: ft.Page):
    page.title = "Weather"
    page.theme_mode = ft.ThemeMode.DARK
    

    routes = wa_routes.Routes
            
    

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = routes(page).route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)