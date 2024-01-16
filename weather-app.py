import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, NavigationDestination, Container, IconButton



import wa_routes

def main(page: ft.Page):
    page.title = "Weather"
    page.window_min_width = 1100
    page.window_min_height = 600



    

    def route_change(route):
        wa_routes.route_change(page,route)

    
        
        

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)