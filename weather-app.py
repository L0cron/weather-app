import flet as ft



import wa_routes

def main(page: ft.Page):
    page.title = "Weather"
    page.theme_mode = ft.ThemeMode.DARK

    page.window_min_width = 1250
    page.window_min_height = 760
    
    page.window_width = page.window_min_width
    page.window_height = page.window_min_height

    routes = wa_routes.Routes
            
    

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = routes(page).route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)