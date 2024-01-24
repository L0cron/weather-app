import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, NavigationDestination
import sqlite3
import datetime





class Routes():
    # User login
    email:str = None
    password:str = None
    logged_in:bool = False


    # App variables

    file_picker = ft.FilePicker()

    bottomABhgt = 75

    active_button = 0


    page:ft.Page = None
    d_or_l:str = 'dark'

    def __init__(self, page) -> None:
        self.page = page
        self.page.overlay.append(self.file_picker)
    
    
    # Search button  
    
    def search(self):
        search_button = ft.ElevatedButton(
            "Выбрать местоположение",
            icon=ft.icons.CALENDAR_MONTH,
            height = 75,
            style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=0), bgcolor=colors.SURFACE_VARIANT),
        )

        return search_button
    
      
    # Date picker
    
    def date_change(self):
        def change_date(e):
            print(f"Date picker changed, value is {date_picker.value}")

        def date_picker_dismissed(e):
            print(f"Date picker dismissed, value is {date_picker.value}")

        date_picker = ft.DatePicker(
            on_change=change_date,
            on_dismiss=date_picker_dismissed,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )

        self.page.overlay.append(date_picker)

        date_button = ft.ElevatedButton(
            "Изменить дату",
            icon=ft.icons.CALENDAR_MONTH,
            height = 75,
            style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=0), bgcolor=colors.SURFACE_VARIANT),
            on_click=lambda _: date_picker.pick_date(),
        )

        return date_button
    
    
    # AppBars
        
    def topAppBar(self, name:str)->AppBar:
        return AppBar(title=Text(name), bgcolor=colors.SURFACE_VARIANT,
            actions = [ft.Row(
                    alignment = ft.MainAxisAlignment.CENTER,
                    spacing = 2,
                    controls = [ft.Container(width = 250, bgcolor = colors.SURFACE_VARIANT, 
                                content=self.date_change()),
                    ft.Container(width = 250, bgcolor = colors.SURFACE_VARIANT, 
                                content=self.search()),
                    
                    ft.PopupMenuButton(
                    items=[
                        ElevatedButton(icon = ft.icons.SETTINGS, text = 'Настройки', color = ft.colors.BLACK, on_click=self.go_to_settings),
                        ft.PopupMenuItem(),
                    ]),
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

            normalColor = ft.colors.SURFACE_VARIANT
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
        controls = [
                self.topAppBar("Мониторинг"),
            
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
        
    def connect_and_sign_in(self,email, password):
        con = sqlite3.connect("./database.db")
        cur = con.cursor()
        found = cur.execute(f"""SELECT * FROM users WHERE email="{email}" AND password="{password}\"""").fetchone()
        if found == None:
            return False
        else:
            return True
        
    def login(self, e):
        e.control.disabled = True
        self.page.update()
        got = self.connect_and_sign_in(self.email,self.password)
        
        e.control.disabled = False
        self.page.update()

        if got == True:
            print("Login succeeded")
            self.logged_in = True
            self.goto(self.upload)
        else:
            print("Login failed")
        

    def email_change(self, e):
        self.email = e.control.value
    def pass_change(self, e):
        self.password = e.control.value

    def login_form(self):
        
        
        
        t1 = ft.TextField(label="Email",width=400,max_length=50, max_lines=1, on_change=self.email_change)
        t2 = ft.TextField(label="Пароль", width=400, max_length=50, max_lines=1, password=True, can_reveal_password=True,on_change=self.pass_change)
        return ft.Container(content=
            ft.Column(controls=[
                t1,
                t2,
                ft.ElevatedButton(color=ft.colors.WHITE, bgcolor=ft.colors.PRIMARY_CONTAINER, text="Войти", on_click=self.login)
            ]
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.all(25)
        
        )
     
    
    def get_file_from_url(self, e):
        return

    def upload_form(self):
        tp = ft.TextField(label='URL', width=700,max_lines=1,on_change=self.get_file_from_url)
        return ft.Container(content=
            ft.Column(controls=[
                ft.ElevatedButton("Выберите файлы",on_click=lambda _: self.file_picker.pick_files(allow_multiple=False, allowed_extensions=["csv", "xlsx"])),
                ft.Text("-- Или --"),
                tp
            ]),
            alignment=ft.alignment.center
        
        )

    def upload(self):

        form = self.login_form()

        if self.logged_in == True:
            form = self.upload_form()

        controls = [
                self.topAppBar("Загрузка файлов"),

                form,

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