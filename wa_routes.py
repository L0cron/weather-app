import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, NavigationDestination
import datetime
import requests




class Routes():
    webserver_url = 'http://localhost:5000'
    # User login
    email:str = ''
    password:str = ''


    # App variables

    file_picker = None

    bottomABhgt = 75

    active_button = 0


    page:ft.Page = None
    d_or_l:str = 'dark'

    def __init__(self, page) -> None:
        self.page = page
        self.file_picker = ft.FilePicker(on_result=self.on_dialog_result)
        self.page.overlay.append(self.file_picker)

        self.file_picker_button.on_click = lambda _: self.file_picker.pick_files(allow_multiple=True, allowed_extensions=["csv", "xlsx"])

    
    


    # Search button  

    city = 'Москва'


    temp = '0' # градусы цельсия
    feels_like = '0' # градусы цельсия
    pressure = '0' # мм рт. ст.
    speed = '0' # м/c
    weather = ""
    
    deg_cel = '℃'

    print1 = ft.Text('', size = 30, color = ft.colors.BLUE_200, bgcolor = ft.colors.with_opacity(0.4, ft.colors.SURFACE_VARIANT))
    print2 = ft.Text('', size = 20,bgcolor = ft.colors.with_opacity(0.4, ft.colors.SURFACE_VARIANT))
    print3 = ft.Text('', size = 25, color = ft.colors.BLUE_200, bgcolor = ft.colors.with_opacity(0.4, ft.colors.SURFACE_VARIANT))
    print4 = ft.Text('', size = 25, color = ft.colors.BLUE_200, bgcolor = ft.colors.with_opacity(0.4, ft.colors.SURFACE_VARIANT))
    print5 = ft.Text('', weight = ft.FontWeight.W_500,size = 30, color = ft.colors.BLUE_200, bgcolor = ft.colors.with_opacity(0.4, ft.colors.SURFACE_VARIANT))

    
    def dropdown_changed(self, e):

        self.city = e.control.value

        #self.page.update()

        city = self.city
        
        #url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
        

        weather_data = requests.get(self.webserver_url+"?city="+self.city).json()

        # self.print1.value = '🌡️ Температура воздуха: '+ str(round(weather_data['main']['temp'])) + ' ℃'
        # self.print2.value  = '      Ощущается как: ' + str(round(weather_data['main']['feels_like'])) + ' ℃'
        # self.print3.value  = '📈 Давление: ' + str(round(weather_data['main']['pressure'])*0.75) + ' мм.рт.ст'
        # self.print4.value  = '💨 Скорость ветра: ' + str(round(weather_data['wind']['speed'])) + ' м/с'
        # self.print5.value  = str(weather_data['weather'][0]['description'])

        self.temp = str(round(weather_data['main']['temp']))
        self.feels_like = str(round(weather_data['main']['feels_like']))
        self.pressure = str(round(weather_data['main']['pressure'])*0.75)
        self.speed = str(round(weather_data['wind']['speed']))
        self.weather = str(weather_data['weather'][0]['description'])
        
        self.monitor()
        self.page.update()

    def search(self):
 
        #t = ft.Text(self.text)
        dd = ft.Dropdown(text_size = 18,hint_style = ft.TextStyle(size = 18, color = ft.colors.PRIMARY), hint_text=self.city,
        on_change=self.dropdown_changed,
        border=0,
        options=[
            ft.dropdown.Option("Амстердам"),
            ft.dropdown.Option("Архангельск"),
            ft.dropdown.Option("Барселона"),
            ft.dropdown.Option("Берлин"),
            ft.dropdown.Option("Буэнос-Айрес"),
            ft.dropdown.Option("Вашингтон"),
            ft.dropdown.Option("Варшава"),
            ft.dropdown.Option("Волгоград"),
            ft.dropdown.Option("Воронеж"),
            ft.dropdown.Option("Вена"),
            ft.dropdown.Option("Детройт"),
            ft.dropdown.Option("Иркутск"),
            ft.dropdown.Option("Калининград"),
            ft.dropdown.Option("Кёльн"),
            ft.dropdown.Option("Копенгаген"),
            ft.dropdown.Option("Лос-Анджелес"),
            ft.dropdown.Option("Мадрид"),
            ft.dropdown.Option("Мурманск"),
            ft.dropdown.Option("Мюнхен"),
            ft.dropdown.Option("Москва"),
            ft.dropdown.Option("Неаполь"),
            ft.dropdown.Option("Нижний Новгород"),
            ft.dropdown.Option("Новосибирск"),
            ft.dropdown.Option("Нью-Йорк"),
            ft.dropdown.Option("Омск"),
            ft.dropdown.Option("Оттава"),
            ft.dropdown.Option("Париж"),
            ft.dropdown.Option("Псков"),
            ft.dropdown.Option("Пермь"),
            ft.dropdown.Option("Рим"),
            ft.dropdown.Option("Рио-де-Жанейро"),
            ft.dropdown.Option("Ростов-на-Дону"),
            ft.dropdown.Option("Сочи"),
            ft.dropdown.Option("Сан-Франциско"),
            ft.dropdown.Option("Санкт-Петербург"),
            ft.dropdown.Option("Стамбул"),
            ft.dropdown.Option("Томск"),
            ft.dropdown.Option("Тегеран"),
            ft.dropdown.Option("Торонто"),
            ft.dropdown.Option("Углич"),
           
        ],
        width=350,
        )

        # a = ft.Column(controls = [ft.Container(margin = 20, width = 2000, height = 70,
        #                                        content = ft.Row(spacing = 80, controls = [dd, self.print5])),
        #                                        ft.Container(margin = 10, content = ft.Column(spacing = 20,  controls = [ft.Column(controls =[self.print1, self.print2]),
        #                                               self.print3, self.print4]))
        #                                                     ])
                                                      
        
        

        return dd
    

    tempTxt = ft.Text('', size = 30)
    tempfeelsTxt = ft.Text('', size = 20)
    pressureTxt = ft.Text('', size = 20)
    windTxt = ft.Text('', size = 20)

    def cards(self):

        self.tempTxt.value = 'Температура на данный момент равняется ' + self.temp + self.deg_cel



        tempCard = ft.Column(width = 3200, controls = [
            ft.Text(self.tempTxt.value, text_align=ft.TextAlign.LEFT, size = 30)],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        alignment=ft.MainAxisAlignment.CENTER
        )



        self.tempfeelsTxt.value = 'Ощущается как ' + self.feels_like + self.deg_cel

        tempfeelsCard = ft.Column(width = 3200, controls=[
            ft.Text(self.tempfeelsTxt.value, text_align=ft.TextAlign.LEFT, size = 20)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        alignment=ft.MainAxisAlignment.CENTER
        )

        temps = ft.Card(content = ft.Row(controls = [ft.Icon(color=ft.colors.PRIMARY, name=ft.icons.DEVICE_THERMOSTAT, size = 50), ft.Column( alignment = ft.MainAxisAlignment.CENTER,controls=[
            tempCard,
            tempfeelsCard
        ],
        spacing=10,
        height=130,
        
        )
        ]
        ))

        
        self.pressureTxt.value = 'Давление равно ' + self.pressure + " мм рт. ст."
        
        pressureCard = ft.Card(content=ft.Column(controls=[
            ft.Icon(ft.icons.COMPRESS,color=ft.colors.PRIMARY, size=50),
            ft.Text(self.pressureTxt.value, text_align=ft.TextAlign.CENTER,  size = 20)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
        ),width=400, height=130)



        self.windTxt.value= 'Скорость ветра равна ' + self.pressure + " м/c"
        
        windCard = ft.Card(content=ft.Column(controls=[
            ft.Icon(ft.icons.WIND_POWER_OUTLINED,color=ft.colors.PRIMARY, size=50),
            ft.Text(self.windTxt.value, text_align=ft.TextAlign.CENTER, size = 20)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
        ),width=400, height=130)
        


        d = ft.Column(controls=[temps, pressureCard, windCard
        ],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        width=3200
        )


        return d


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
    def close_banner(self):
        self.banner.open = False
        self.page.update()


    is_banner_shown = False
    def switch_banner(self, e):
        if self.is_banner_shown == False:
            self.is_banner_shown = True
            print(self.is_banner_shown)

        self.page.update()
        
        
         
    def topAppBar(self, name:str)->AppBar:

        login_button = ElevatedButton(icon = ft.icons.ACCOUNT_CIRCLE, text = 'Войти', color = ft.colors.BLACK, on_click=self.go_to_upload)

        if self.login_status == 1:
            login_button.text = "Выйти"
            login_button.icon = ft.icons.LOGOUT
            login_button.on_click = self.logout

        return AppBar(title=Text(name), bgcolor=colors.SURFACE_VARIANT,
            actions = [ft.Row(
                    alignment = ft.MainAxisAlignment.CENTER,
                    spacing = 2,
                    controls = [ft.Container(width = 250, bgcolor = colors.SURFACE_VARIANT, 
                                content=self.date_change()),
                    
                    self.search(),
                    ft.IconButton(icon = ft.icons.NOTIFICATIONS_ON_OUTLINED, on_click = self.switch_banner),
                    ft.PopupMenuButton(
                    items=[
                        ElevatedButton(icon = ft.icons.SETTINGS, text = 'Настройки', color = ft.colors.BLACK, on_click=self.go_to_settings),
                        login_button,
                        ft.PopupMenuItem(),
                    ]),
                    ]
                ),
            ]
        )
    
        
    def colorSchemes(self)->list:
        invColor = ft.colors.PRIMARY
        invTextColor = ft.colors.WHITE
        
        normalColor = ft.colors.SURFACE_VARIANT
        normalTxtColor = ft.colors.PRIMARY
        
        if self.d_or_l == 'dark':
            invColor = ft.colors.PRIMARY_CONTAINER
            invTextColor = ft.colors.WHITE

            normalColor = ft.colors.SURFACE_VARIANT
            normalTxtColor = ft.colors.WHITE

        return [normalColor, normalTxtColor, invColor, invTextColor]

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
                        ElevatedButton(icon = ft.icons.WB_SUNNY_OUTLINED, text = 'Сменить тему', height = 50, width = 200, on_click = self.change_theme_),
                        ft.Switch(label="Уведомления", value=True,thumb_color={ft.MaterialState.SELECTED: ft.colors.PRIMARY},track_color=ft.colors.SURFACE_VARIANT,focus_color=ft.colors.PURPLE)
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


    # Notify

    def notify(self):
        banner = ft.Banner(
            bgcolor=ft.colors.PRIMARY,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                "Oops, there were some errors while trying to delete the file. What would you like me to do?",
                color = ft.colors.BLACK
            ),
            actions=[
                ft.TextButton("Retry", on_click=self.close_banner)
            ],
            open=self.is_banner_shown
        )
        print('notify',self.is_banner_shown)
        return banner

    # Monitoring and GOTO monitoring

    def monitor(self):
        controls = [
                self.topAppBar("Мониторинг"),
                self.cards(),
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
        
    def graphics(self):
        items = ['вова лох']*20
        col = ft.Column(controls=[ft.Text(value=i) for i in items])
        return col
    
    def analyze(self):
  
        controls = [
                self.topAppBar("Анализ и виузализация"),
                self.graphics(),
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
        try:
            re = requests.request(url=self.webserver_url, method='GET', params={"email":email,"password":password})
            response = str(re.content)[2:-1]
            if response == 'success':
                return 1
            else:
                return 0
        except:
            return -1
        

    def logout(self, e):
        self.login_status = 0
        
        self.email = ''
        self.password = ''

        self.go_to_monitor(e)
        
    def login(self, e):
        if self.email == '' or self.password == '':
            return
        e.control.disabled = True
        self.page.update()
        got = self.connect_and_sign_in(str(self.email),str(self.password))
        
        e.control.disabled = False
        self.page.update()

        if got == -1:
            self.email = ''
            self.password = ''
            print("Ошибка сервера")
            self.login_status = -1
            self.goto(self.upload)
            
        elif got == 0:
            self.email = ''
            self.password = ''
            print("Неверный логин или пароль")
            self.login_status = 2
            self.goto(self.upload)
        elif got == 1:
            print("Успешный вход")
            self.login_status = 1
            self.goto(self.upload)
        

    login_status = 0
    # 0 - ничего
    # 1 - успешно
    # 2 - неверные данные
    # -1 - ошибка сервера

    def email_change(self, e):
        self.email = str(e.control.value)
    def pass_change(self, e):
        self.password = str(e.control.value)

    def login_form(self):

        base_color = ft.colors.PRIMARY_CONTAINER
        if self.d_or_l != 'dark':
            base_color = ft.colors.PRIMARY
        txt = ft.Text(text_align=ft.TextAlign.CENTER,width=400)
        if self.login_status == -1:
            txt.value = "Сервер не отвечает, попробуйте позже."
            txt.color = ft.colors.RED
        elif self.login_status == 2:
            txt.value = "Неверный логин или пароль."
            txt.color = ft.colors.RED
        
        t1 = ft.TextField(label="Email",width=400,max_length=50, max_lines=1, on_change=self.email_change)
        t2 = ft.TextField(label="Пароль", width=400, max_length=50, max_lines=1, password=True, can_reveal_password=True,on_change=self.pass_change)
        return ft.Row(controls=[
            ft.Column(controls=[
                t1,
                t2,
                ft.Row(controls=[
                    ft.Column(controls=[
                        ft.ElevatedButton(color=ft.colors.WHITE, bgcolor=base_color, text="Войти", on_click=self.login, width=100),
                        txt
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ],
                width=400,
                alignment=ft.MainAxisAlignment.CENTER
                )
            ]
            )],
            alignment=ft.MainAxisAlignment.CENTER,
            )
     
    
    file_upload_url = ''
    def get_file_from_url(self, e):
        self.file_upload_url = e.control.value

    file_picker_button = ft.ElevatedButton("Выберите файлы", style=ft.ButtonStyle(shape = ft.BeveledRectangleBorder(radius=0)))
    file_upload_button = ft.ElevatedButton("Выгрузить", style=ft.ButtonStyle(shape = ft.BeveledRectangleBorder(radius=0)), height=50, width=200)

    def on_dialog_result(self, e: ft.FilePickerResultEvent):
        self.do_upload(files=e.files)

    def do_upload(self, files:list=None, url:str=None):
        if files == None and url == None:
            return
        self.file_picker_button.disabled = True
        self.file_upload_button.disabled = True
        self.page.update()

        print("We are connecting to a website")
        
        nfiles = {}
        for i in range(len(files)):
            nfiles[f"file{i}"] = open(files[i].path, 'rb')

        print(nfiles)

        re = None
        if files != None:
            re = requests.request(url=self.webserver_url, method="post", files=nfiles)
        elif url != None:
            return
        
        re.content
        
        self.file_picker_button.disabled = False
        self.file_upload_button.disabled = False
        self.page.update()

    def upload_form(self):
        tp = ft.TextField(label='URL', width=600,max_lines=1,on_change=self.get_file_from_url)
        return ft.Column(controls=[
                self.file_picker_button,
                ft.Divider(),
                ft.Row(controls=[
                    tp,
                    self.file_upload_button
                ],
                width=810,
                spacing=10
                )
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=810
            )
            
        
        
    def upload(self):

        form = self.login_form()

        if self.login_status == 1:
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