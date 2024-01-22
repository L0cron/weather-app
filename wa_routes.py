import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, NavigationDestination




class Routes():

    bottomABhgt = 75

    active_button = 0


    page:ft.Page = None
    d_or_l:str = 'dark'

    def __init__(self, page) -> None:
        
        self.page = page

    # AppBars
        
    def topAppBar(self, name:str)->AppBar:
        return AppBar(title=Text(name), bgcolor=colors.SURFACE_VARIANT,
            actions = [
                    ft.PopupMenuButton(
                    items=[
                        ElevatedButton(icon = ft.icons.SETTINGS, text = 'Настройки', color = ft.colors.BLACK, on_click=self.go_to_settings),
                        ft.PopupMenuItem(),
                    ]
                ),
            ]
        )
    
        


    def bottomAppBar(self)->AppBar:
        hgt = self.bottomABhgt

        regularButtonStyle = ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=0))

        invColor = ft.colors.PRIMARY
        textColor = ft.colors.WHITE
        
        normalColor = ft.colors.SURFACE_VARIANT
        normalTxtColor = ft.colors.PRIMARY
        
        if self.d_or_l == 'dark':
            invColor = ft.colors.PRIMARY_CONTAINER
            textColor = ft.colors.WHITE

            normalColor = ft.colors.BLACK
            normalTxtColor = ft.colors.WHITE
            
        buttons = [
                        ft.ElevatedButton(color=normalTxtColor, bgcolor=normalColor,icon=ft.icons.HOME_ROUNDED, text="Мониторинг", style=regularButtonStyle,expand=True,height=hgt,on_click=self.go_to_monitor),
                        ft.ElevatedButton(color=normalTxtColor, bgcolor=normalColor,icon=ft.icons.BAR_CHART_ROUNDED, text="Анализ и Визуализация", style=regularButtonStyle,expand=True,height=hgt,on_click=self.go_to_analyze),
                        ft.ElevatedButton(color=normalTxtColor, bgcolor=normalColor, icon=ft.icons.WB_SUNNY_OUTLINED, text="Прогнозирование", style=regularButtonStyle,expand=True,height=hgt, on_click = self.go_to_prediction),
                        ft.ElevatedButton(color=normalTxtColor, bgcolor=normalColor, icon=ft.icons.CLOUD_UPLOAD_OUTLINED, text="Загрузка файлов", style=regularButtonStyle,expand=True,height=hgt, on_click=self.go_to_upload),
        ]

        active = self.active_button
        for i in range(len(buttons)):
            if i == active:
                buttons[i].color = textColor
                buttons[i].bgcolor = invColor
                break

        btmBar= ft.BottomAppBar(
                    height=hgt,
                    padding=0,
                    content=ft.Row(controls=buttons,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY
                    )
                )
        
        return btmBar


    def dotsPopupMenu(self):
        return ft.PopupMenuButton(
                            items=[
                                ElevatedButton(icon = ft.icons.SETTINGS, text = 'Настройки', color = ft.colors.BLACK, on_click=self.go_to_settings)
                            ]   
                        )

    def go_to_settings(self, e):
        self.page.go("/settings")
        self.page.views.append(
                View(
                    "/settings", 
                    [
                        AppBar(title=Text("Настройки"), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton(icon = ft.icons.WB_SUNNY_OUTLINED, text = 'Сменить тему', on_click = self.change_theme_),
                    ],
                )
            )
        self.page.update()


    def change_theme_(self,e):
        if self.d_or_l == 'dark':
            self.d_or_l = 'light'
            self.page.theme_mode = ft.ThemeMode.LIGHT

        elif self.d_or_l == 'light':
            self.d_or_l = 'dark' 
            self.page.theme_mode = ft.ThemeMode.DARK
        self.page.update()

    def check_item_clicked(self, e):
        e.control.checked = not e.control.checked
        self.page.update()
    # GOTO
    

    # Monitoring and GOTO monitoring

    def monitor(self):
        controls = [AppBar(
                    leading_width=40,
                    title=Text("Погода в городе " + "Москва", color=ft.colors.PRIMARY, weight=ft.FontWeight.W_600),
                    center_title=False,
                    bgcolor=colors.SURFACE_VARIANT,
                    actions=[
                        self.dotsPopupMenu()
                    ],
                ),
                self.bottomAppBar()
            ]
        return controls
    

    def go_to_monitor(self, e):
        self.page.update()
        if self.active_button != 0:
            self.active_button = 0
            self.goto(self.monitor)
        self.page.update()

    # Analyze and GOTO analyze

    def analyze(self):
        controls = [
                self.topAppBar("Анализ и виузализация"),
            
                self.bottomAppBar()
            ]
        return controls

    def go_to_analyze(self, e):
        self.page.update()
        if self.active_button != 1:
            self.active_button = 1
            self.goto(self.analyze)
            
        self.page.update()


    # Prediction and GOTO prediction

    def prediction(self):
        controls = [
                self.topAppBar("Прогнозирование"),
            
                self.bottomAppBar()
            ]
        return controls


    def go_to_prediction(self, e):
        self.page.update()
        if self.active_button != 2:
            self.active_button = 2
            self.goto(self.prediction)
        self.page.update()

    # Upload and GOTO upload

    def upload(self):
        controls = [
                self.topAppBar("Загрузка файлов"),
                self.bottomAppBar()
            ]
        return controls

    def go_to_upload(self, e):
        self.page.update()
        if self.active_button != 3:
            self.active_button = 3
            self.goto(self.upload)
        self.page.update()


    

    def goto(self, where):

        self.page.views.clear()
        self.page.views.append(
            View(
                "/",
                where()
        ))
        
        self.page.update()
    



    def route_change(self, route):

        func = None

        if self.active_button == 0:
            func = self.monitor
        elif self.active_button == 1:
            func = self.analyze
        elif self.active_button == 2:
            func = self.prediction
        elif self.active_button == 3:
            func = self.upload


        self.page.views.clear()
        self.page.views.append(
            View(
                "/",
                func()
        ))
        
        self.page.update()