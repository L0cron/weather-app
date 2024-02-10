import time
import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, NavigationDestination
import datetime
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from flet.plotly_chart import PlotlyChart
import asyncio


class Routes():

    webserver_url = 'http://localhost:5000'

    # User login
    email:str = ''
    password:str = ''


    # App variables

    file_picker = None

    bottomABhgt = 75

    active_button = 0

    sb:ft.SnackBar = None

    page:ft.Page = None
    d_or_l:str = 'dark'

    graph_1:PlotlyChart=None
    graph_2:PlotlyChart=None
    graph_3:PlotlyChart=None

    def __init__(self, page) -> None:
        self.page = page
        self.file_picker = ft.FilePicker(on_result=self.on_dialog_result)
        self.page.overlay.append(self.file_picker)

        self.file_picker_button.on_click = lambda _: self.file_picker.pick_files(allow_multiple=True, allowed_extensions=["csv", "xlsx"])

    
        self.sb = ft.SnackBar(bgcolor = ft.colors.SECONDARY_CONTAINER,
            content=ft.Container(content = ft.Row(controls = 
            [ft.Icon(name=ft.icons.NOTIFICATIONS_ACTIVE, color=ft.colors.PRIMARY),
            ft.Text("Добрый вечер! В Москве сейчас -2"+self.deg_cel, size = 20, color = ft.colors.PRIMARY)])
            ),
            #action=ft.IconButton(icon = ft.icons.NOTIFICATIONS_ON_OUTLINED, on_click = self.close_banner),
            duration=10000,
            show_close_icon = True,
            close_icon_color = ft.colors.PRIMARY

        )
        self.page:ft.Page

        try:
        
            self.search_init()

            self.do_refresh()
            self.init_complete = True
        except:
            print("Сервер не ответил")

        
        

    
    # Search button  

    city = 'Москва'


    temp = '0' # градусы цельсия
    feels_like = None # градусы цельсия
    pressure = '0' # мм рт. ст.
    humidity = '0' # влажность
    speed = '0' # м/c
    description = "" # описание
    wind_direction = '0' # градусы
    overcast = None # overcast
    
    deg_cel = '℃'
    deg = '°'

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
        

        weather_data = requests.get(self.webserver_url+'/city',params={'city':city,'date':self.date_to_bd_date(self.current_date)})
        if str(weather_data.content)[2:-1] == 'Error':
            return
        
        self.do_refresh()

        self.monitor()
        self.page.update()




    pb_lst = ['Уведомление 1','Уведомление 2','Уведомление 3']
    pb = ft.PopupMenuButton(icon = ft.icons.NOTIFICATIONS_ON_OUTLINED,
        items=[
            ft.PopupMenuItem(
                text="Закрыть",
                icon = ft.icons.EXIT_TO_APP_OUTLINED,
            ),
            #ft.PopupMenuItem(),
        ]
    )
    for i in pb_lst: pb.items.insert(2, (ft.PopupMenuItem(text=i)))

    search_options = []
    def search_init(self):
        cities = requests.get(self.webserver_url+'/cities')
        cities = list(cities.json())
        cities.sort()
        self.search_options = [ft.dropdown.Option(i) for i in cities]
        print(self.search_options)

    def search(self):
        #t = ft.Text(self.text)
        dd = ft.Dropdown(text_size = 18,hint_style = ft.TextStyle(size = 18, color = ft.colors.PRIMARY), hint_text=self.city,
        on_change=self.dropdown_changed,
        border=0,
        options=self.search_options,
        width=350,
        )

        # a = ft.Column(controls = [ft.Container(margin = 20, width = 2000, height = 70,
        #                                        content = ft.Row(spacing = 80, controls = [dd, self.print5])),
        #                                        ft.Container(margin = 10, content = ft.Column(spacing = 20,  controls = [ft.Column(controls =[self.print1, self.print2]),
        #                                               self.print3, self.print4]))
        #                                                     ])
                                                      
        
        
        print(self.city)
        return dd
    

    

    def cards(self):

        temp = 'Температура на данный момент равняется ' + self.temp + self.deg_cel



        tempCard = ft.Column(width = 3200, controls = [
            ft.Text(temp, text_align=ft.TextAlign.LEFT, size = 30)],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        alignment=ft.MainAxisAlignment.CENTER
        )


        var = '0'
        if self.feels_like != None:
            var = self.feels_like
        feels_like = 'Ощущается как ' + var + self.deg_cel
        

        tempfeelsCard = ft.Column(width = 3200, controls=[
            ft.Text(feels_like, text_align=ft.TextAlign.LEFT, size = 20)
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

        
        pressure = 'Давление равно ' + self.pressure + " мм рт. ст."
        
        pressureCard = ft.Card(content=ft.Row(controls=[
            ft.Icon(ft.icons.COMPRESS,color=ft.colors.PRIMARY, size=50),
            ft.Text(pressure, text_align=ft.TextAlign.CENTER,  size = 25)
        ],
        alignment=ft.MainAxisAlignment.START
        ),width=3200, height=130)
        
        
        humidity = 'Влажность равна ' + self.humidity + "%"
        
        
        controls = [ft.Text(humidity, text_align=ft.TextAlign.CENTER,  size = 25)]
        if self.overcast != None:
            overcast = 'Количество осадков равно ' + self.overcast
            controls.append(ft.Text(overcast, text_align=ft.TextAlign.CENTER,  size = 19))



        wetCard = ft.Card(content=ft.Row(controls=[
            ft.Icon(ft.icons.WATER_DROP_ROUNDED,color=ft.colors.PRIMARY, size=50),
            ft.Column(controls = controls,
            alignment = ft.MainAxisAlignment.CENTER)
        ],
        alignment=ft.MainAxisAlignment.START
        ),width=3200, height=130)

        if self.overcast != None:
            wetCard.content



        wind_speed= 'Скорость ветра равна ' + self.speed + " м/c"
        wind_direction= 'Направление ветра ' + self.wind_direction + self.deg
        windCard = ft.Card(content=ft.Row(controls=[
            ft.Icon(ft.icons.WIND_POWER_OUTLINED,color=ft.colors.PRIMARY, size=50),
            ft.Column(controls = [ft.Text(wind_speed, text_align=ft.TextAlign.CENTER, size = 25),
            ft.Text(wind_direction, text_align=ft.TextAlign.CENTER, size = 19)], alignment = ft.MainAxisAlignment.CENTER)
        ],
        alignment=ft.MainAxisAlignment.START
        ),width=3200, height=130)
        
        
        
        d = ft.Column(controls=[temps,                       
                                pressureCard,
                                 windCard,
                                  wetCard,
                                  ],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        width=3200)
        


        return d
    
    def date_to_bd_date(self, date:datetime.datetime): # 2024-02-10 YYYY-MM-DD -> (D)D.(M)M.YYYY
        
        d = str(date).split()[0].split('-')

        result = []
        for i in d:
            k = i
            for j in i:
                if j != '0':
                    break
                else:
                    k = k[1:]
            result.append(k)

        print('.'.join(result[::-1]))
        return '.'.join(result[::-1])

    init_complete = False

    def do_refresh(self):
        print("Refreshing...")
        print('data changed to', self.current_date)

        self.refresher_active = True

        if self.active_button == 0:
            self.goto(self.monitor)
        elif self.active_button == 1:
            self.goto(self.analyze)
        elif self.active_button == 2:
            self.goto(self.prediction)
        elif self.active_button == 3:
            self.goto(self.upload)
        self.page.update()

        date = self.date_to_bd_date(self.current_date)

        city = self.city

        if self.init_complete == False:
            try:
                self.search_init()
                self.init_complete = True
            except:
                print("Сервер не отвечает")
                self.refresher_active = False
                if self.active_button == 0:
                    self.goto(self.monitor)
                elif self.active_button == 1:
                    self.graphics()
                    self.goto(self.analyze)
                elif self.active_button == 2:
                    self.goto(self.prediction)
                elif self.active_button == 3:
                    self.goto(self.upload)
                self.page.update()
                return

        last = requests.get(url=self.webserver_url+"/city", params={"city":city,"date":date}).json()[-1]
        print(last)

        for i in range(len(last)):
            if last[i] != None:
                last[i] = str(last[i])

        self.temp = last[4]
        self.feels_like = last[5]
        self.pressure = last[6]
        self.humidity = last[7]
        self.description = last[8]
        self.wind_direction = last[9]
        self.speed = last[10]
        self.overcast = last[11]


        self.refresher_active = False
        if self.active_button == 0:
            self.goto(self.monitor)
        elif self.active_button == 1:
            self.graphics()
            self.goto(self.analyze)
        elif self.active_button == 2:
            self.goto(self.prediction)
        elif self.active_button == 3:
            self.goto(self.upload)
        #self.go_to_prediction(e)
        self.page.update()

    def refresh_button_pressed(self, e):
        self.do_refresh()

    # Date picker
    current_date = datetime.date.today()
    server_did_not_respond = False
    # actual_time = str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute)
    def date_change(self):
        def change_date(e):
            print(f"Date picker changed, value is {date_picker.value}")
            self.current_date = date_picker.value
            print('data changed to', self.current_date)
            if self.active_button == 0:
                self.goto(self.monitor)
            elif self.active_button == 1:
                self.goto(self.analyze)
            elif self.active_button == 2:
                self.goto(self.prediction)
            elif self.active_button == 3:
                self.goto(self.upload)
            #self.go_to_prediction(e)
            self.page.update()
            
        def date_picker_dismissed(e):
            print(f"Date picker dismissed, value is {date_picker.value}")
            self.current_date = date_picker.value
            self.page.update()
            
        date_picker = ft.DatePicker(
            on_change=change_date,
            on_dismiss=date_picker_dismissed,
            first_date=datetime.date(1990, 10, 1),
            last_date=datetime.date(2025, 10, 1),
            value = self.current_date
        )

        self.page.overlay.append(date_picker)

        date_button = ft.ElevatedButton(
            "Изменить дату",
            icon=ft.icons.CALENDAR_MONTH,
            height = 75,
            width = 300,
            style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=0), bgcolor=colors.SURFACE_VARIANT),
            on_click=lambda _: date_picker.pick_date(),
        )
        self.page.update()
        return date_button

    
    # AppBars
    def close_banner(self):
        self.notifications = False
        self.sb.open = False
        self.page.update()



    is_banner_shown = False

    def switch_banner(self, e):
        if self.notifications == True:
            self.sb.open = True
            self.notifications = True
            self.page.update()
            time.sleep(5)
            self.sb.open = False
            self.page.update()

        
        
         
    def topAppBar(self, name:str)->AppBar:

        login_button = ElevatedButton(icon = ft.icons.ACCOUNT_CIRCLE, text = 'Войти', color = ft.colors.BLACK, on_click=self.go_to_upload)

        if self.login_status == 1:
            login_button.text = "Выйти"
            login_button.icon = ft.icons.LOGOUT
            login_button.on_click = self.logout
        self.page.update()
        
        text = str('Актуально на '+str(self.date_to_bd_date(self.current_date)))
        if self.init_complete == False:
            text = 'Сервер не отвечает.'

        dateCard = ft.Card(content=ft.Row(controls=[ft.Text('  '),
            ft.Row(controls=[
                ft.Row(controls=[
                    ft.Icon(ft.icons.ACCESS_TIME,color=ft.colors.PRIMARY, size=20),
                    ft.Text(text, text_align=ft.TextAlign.LEFT, size = 20),
                ],alignment=ft.MainAxisAlignment.START),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ],
        alignment = ft.MainAxisAlignment.START
        ),width=300, height = 300, color = ft.colors.SURFACE_VARIANT)
        
        
        return AppBar(title=Text(name), bgcolor=colors.SURFACE_VARIANT,
            actions = [ft.Row(
                    alignment = ft.MainAxisAlignment.CENTER,
                    spacing = 4,
                    controls = [dateCard,
                                 ft.Container(width = 250, bgcolor = colors.SURFACE_VARIANT, 
                                content=self.date_change()),
                    
                    self.search(),
                    #ft.IconButton(icon = ft.icons.NOTIFICATIONS_ON_OUTLINED, on_click = self.switch_banner),
                    self.pb,
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

    refresher_active = False
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

        refresher = ft.AlertDialog(
            modal=True,
            title=ft.Row(controls=[ft.ProgressRing(width=25, height=25, stroke_width = 2),ft.Text("Обновляем данные...")]),
            content=ft.Row(controls = [ft.Text("Устанавливаем связь с сервером...")
            ]),
            actions_alignment=ft.MainAxisAlignment.END,
            open=False,
        )

        if self.refresher_active:
            refresher.open = True
            
        buttons = [
                        ft.ElevatedButton(color=normalTxtColor, bgcolor=normalColor,icon=ft.icons.HOME_ROUNDED, text="Мониторинг", style=regularButtonStyle,expand=True,height=hgt,on_click=self.go_to_monitor),
                        ft.ElevatedButton(color=normalTxtColor, bgcolor=normalColor,icon=ft.icons.BAR_CHART_ROUNDED, text="Анализ и Визуализация", style=regularButtonStyle,expand=True,height=hgt,on_click=self.go_to_analyze),
                        ft.ElevatedButton(color=normalTxtColor, bgcolor=normalColor, icon=ft.icons.WB_SUNNY_OUTLINED, text="Прогнозирование", style=regularButtonStyle,expand=True,height=hgt, on_click = self.go_to_prediction),
                        ft.ElevatedButton(color=normalTxtColor, bgcolor=normalColor, icon=ft.icons.CLOUD_UPLOAD_OUTLINED, text="Загрузка файлов", style=regularButtonStyle,expand=True,height=hgt, on_click=self.go_to_upload),
                        refresher
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
    
    notifications = True
    def set_notifications(self, e:ft.ControlEvent):
        self.notifications = e.control.value

    is_registering = False
    def go_to_register(self, e):
        self.login_status = 0
        self.page.update()
        if self.is_registering == False:
            self.is_registering = True
            self.goto(self.upload, True)
        self.page.update()
    
    def go_to_settings(self, e):
        self.page.go("/settings")
        self.page.views.append(
                View(
                    "/settings", 
                    [
                        AppBar(title=Text("Настройки"), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton(icon = ft.icons.WB_SUNNY_OUTLINED, text = 'Сменить тему', height = 50, width = 200, on_click = self.change_theme_),
                        ft.Switch(label="Уведомления", value=True,thumb_color=ft.colors.PRIMARY,track_color=ft.colors.SURFACE_VARIANT,on_change=self.set_notifications)
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
    
    def notify_user(self,e):
        if self.notifications == True:
            
            self.sb.open = True
            self.page.update()
            #self.sb.open = False
        else:
            print("У пользователя отключены уведомления")
    
    # Monitoring and GOTO monitoring

    def make_refresh(self):
        a = ft.FloatingActionButton(
                    icon=ft.icons.REFRESH_ROUNDED, on_click=self.refresh_button_pressed, bgcolor=ft.colors.BLUE )
        return a
    dat = floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, text = 'loool', bgcolor=ft.colors.LIME_300)
    def monitor(self):
        controls = [
                self.topAppBar("Мониторинг"),
                self.cards(),
                self.bottomAppBar(),
                self.sb,
                self.make_refresh()
            ]
        
        return controls
    

    def go_to_monitor(self, e):
        self.page.update()
        if self.active_button != 0:
            self.active_button = 0
            self.goto(self.monitor)
        self.page.update()

    # Analyze and GOTO analyze
        
    # Graphics

    def graphics(self):
        def filter_(days):
            days = list(date.split(' ') for date in days)
            woof_days = []
            for i in days:
                a = i[1].replace('.', '-')
                woof_days.append(a + ' ' + i[0])
            return woof_days
        
        # Reading CSV files into Pandas DataFrames
        anime = pd.read_csv('./serverside/sanya/1.csv', low_memory=False, index_col=0, sep=',')
        anime2 = pd.read_csv('./serverside/sanya/2.csv', low_memory=False, index_col=0, sep=',')
        anime3 = pd.read_csv('./serverside/sanya/3.csv', low_memory=False, index_col=0, sep=',')
        
        # Processing data from anime
        days = filter_(anime['время'].values)
        temperatures = anime['температура_воздуха_по_сухому_термометру'].values[:90:]
        humidities = anime['относительная_влажность_воздуха'].values[:90:]
        pressures = anime['атмосферное_давление_на_уровне_станции'].values[:90:]
        
        if anime['температура_воздуха_по_сухому_термометру'].values[90] > anime['температура_воздуха_по_сухому_термометру'].values[0]:
            self.temp_fact = 'Общее повышение температуры'
        else:
            self.temp_fact = 'Общее понижение температуры'
        
        if anime['относительная_влажность_воздуха'].values[90] > anime['относительная_влажность_воздуха'].values[0]:
            self.wet_fact = 'Общее повышение влажности'
        else:
            self.wet_fact = 'Общее понижение влажности'
            
        
        if anime['атмосферное_давление_на_уровне_станции'].values[90] > anime['атмосферное_давление_на_уровне_станции'].values[0]:
            self.press_fact = 'Общее повышение давления'
        else:
            self.press_fact = 'Общее понижение давления'
            
            
        datetime_objects = [datetime.datetime.strptime(dt_string, '%d-%m-%Y %H:%M') for dt_string in days][:90:]
        

        # Processing data from anime2
        days2 = filter_(anime2['время'].values)
        temperatures2 = anime2['температура_воздуха_по_сухому_термометру'].values[:90:]
        humidities2 = anime2['относительная_влажность_воздуха'].values[:90:]
        pressures2 = anime2['атмосферное_давление_на_уровне_станции'].values[:90:]
        datetime_objects2 = [datetime.datetime.strptime(dt_string, '%d-%m-%Y %H:%M') for dt_string in days][:90:]
        
        if anime2['температура_воздуха_по_сухому_термометру'].values[90] > anime2['температура_воздуха_по_сухому_термометру'].values[0]:
            self.temp_fact2 = 'Общее повышение температуры'
        else:
            self.temp_fact2 = 'Общее понижение температуры'
        
        if anime2['относительная_влажность_воздуха'].values[90] > anime2['относительная_влажность_воздуха'].values[0]:
            self.wet_fact2 = 'Общее повышение влажности'
        else:
            self.wet_fact2 = 'Общее понижение влажности' 
            
        if anime2['атмосферное_давление_на_уровне_станции'].values[90] > anime2['атмосферное_давление_на_уровне_станции'].values[0]:
            self.press_fact2 = 'Общее повышение давления'
        else:
            self.press_fact2 = 'Общее понижение давления'  
   
        # Processing data from anime3
        days3 = filter_(anime3['время'].values)
        temperatures3 = anime3['температура_воздуха_по_сухому_термометру'].values[:90:]
        humidities3 = anime3['относительная_влажность_воздуха'].values[:90:]
        pressures3 = anime3['атмосферное_давление_на_уровне_станции'].values[:90:]
        datetime_objects3 = [datetime.datetime.strptime(dt_string, '%d-%m-%Y %H:%M') for dt_string in days][:90:]

        if anime3['температура_воздуха_по_сухому_термометру'].values[90] > anime3['температура_воздуха_по_сухому_термометру'].values[0]:
            self.temp_fact3 = 'Общее повышение температуры'
        else:
            self.temp_fact3 = 'Общее понижение температуры'
        
        if anime3['относительная_влажность_воздуха'].values[90] > anime3['относительная_влажность_воздуха'].values[0]:
            self.wet_fact3 = 'Общее повышение влажности'
        else:
            self.wet_fact3 = 'Общее понижение влажности' 
            
        if anime3['атмосферное_давление_на_уровне_станции'].values[90] > anime3['атмосферное_давление_на_уровне_станции'].values[0]:
            self.press_fact3 = 'Общее повышение давления'
        else:
            self.press_fact3 = 'Общее понижение давления' 
 
        # Построение графика с использованием Plotly
        fig = go.Figure()

        # Добавляем график для температуры на ось Y1
        fig.add_trace(go.Scatter(x=datetime_objects, y=temperatures, mode='lines', name='Температура'))

        # Добавляем график для влажности на ось Y2
        fig.add_trace(go.Scatter(x=datetime_objects, y=humidities, mode='lines', name='Влажность', yaxis='y2'))

        # Добавляем график для давления на ось Y3
        fig.add_trace(go.Scatter(x=datetime_objects, y=pressures, mode='lines', name='Давление', yaxis='y3'))

        # Настройка меток осей и заголовка
        fig.update_layout(title=None,
                        yaxis=dict(title=None, side='left', showgrid=True, zeroline=True, showticklabels=True),
                        yaxis2=dict(title=None, side='right', overlaying='y', showgrid=False, zeroline=False, showticklabels=False),
                        yaxis3=dict(title=None, side='right', overlaying='y', showgrid=False, zeroline=False, showticklabels=False),
                        xaxis=dict(title=None, showticklabels=False),
                        height=300,  # Установка высоты графика
                        width=400,
                        showlegend=False,
                        margin=dict(l=0,r=0,b=0,t=0),
                        paper_bgcolor="#F0F8FF")
        
        # Построение графика с использованием Plotly
        fig2 = go.Figure()

        # Добавляем график для температуры на ось Y1
        fig2.add_trace(go.Scatter(x=datetime_objects2, y=temperatures2, mode='lines', name='Температура', yaxis='y1'))

        # Добавляем график для влажности на ось Y2
        fig2.add_trace(go.Scatter(x=datetime_objects2, y=humidities2, mode='lines', name='Влажность', yaxis='y2'))

        # Добавляем график для давления на ось Y3
        fig2.add_trace(go.Scatter(x=datetime_objects2, y=pressures2, mode='lines', name='Давление', yaxis='y3'))

        # Настройка меток осей и заголовка
        fig2.update_layout(title=None,
                        yaxis=dict(title=None, side='left', showgrid=True, zeroline=True, showticklabels=True),
                        yaxis2=dict(title=None, side='right', overlaying='y', showgrid=False, zeroline=False, showticklabels=False),
                        yaxis3=dict(title=None, side='right', overlaying='y', showgrid=False, zeroline=False, showticklabels=False),
                        xaxis=dict(title=None, showticklabels=False),
                        height=300,  # Установка высоты графика
                        width=400,
                        showlegend=False,
                        margin=dict(l=0,r=0,b=0,t=0),
                        paper_bgcolor="#F0F8FF")
        
        # Построение графика с использованием Plotly
        fig3 = go.Figure()

        # Добавляем график для температуры на ось Y1
        fig3.add_trace(go.Scatter(x=datetime_objects3, y=temperatures3, mode='lines', name='Температура', yaxis='y1'))

        # Добавляем график для влажности на ось Y2
        fig3.add_trace(go.Scatter(x=datetime_objects3, y=humidities3, mode='lines', name='Влажность', yaxis='y2'))

        # Добавляем график для давления на ось Y3
        fig3.add_trace(go.Scatter(x=datetime_objects3, y=pressures3, mode='lines', name='Давление', yaxis='y3'))

        # Настройка меток осей и заголовка
        fig3.update_layout(title=None,
                        yaxis=dict(title=None, side='left', showgrid=True, zeroline=True, showticklabels=True),
                        yaxis2=dict(title=None, side='right', overlaying='y', showgrid=False, zeroline=True, showticklabels=False),
                        yaxis3=dict(title=None, side='right', overlaying='y', showgrid=False, zeroline=True, showticklabels=False),
                        xaxis=dict(title=None, showticklabels=False),
                        height=300,  # Установка высоты графика
                        width=400,
                        showlegend=False,
                        margin=dict(l=0,r=0,b=0,t=0),
                        paper_bgcolor="#F0F8FF")
        
        self.graph_1 = PlotlyChart(fig, expand=True, isolated=False,)
        self.graph_2 = PlotlyChart(fig2, expand=True, isolated=False,)
        self.graph_3 = PlotlyChart(fig3, expand=True, isolated=False,)
        self.load_graphics = 2

        self.page.update()
        
    
    def grafics_card2(self):
 
        a = ft.Container(content = ft.Card(content = ft.Row(
            controls =
            [ft.Row(controls = [ ft.Icon(name=ft.icons.CIRCLE, color=ft.colors.BLUE, size=30), ft.Text('Температура', size = 30)]),   
            ft.Row(controls = [ ft.Icon(name=ft.icons.CIRCLE, color=ft.colors.RED, size=30), ft.Text('Влажность', size = 30)]),  
            ft.Row(controls = [ ft.Icon(name=ft.icons.CIRCLE, color=ft.colors.GREEN, size=30), ft.Text('Давление', size = 30)])],
            alignment = ft.MainAxisAlignment.SPACE_AROUND
               
        ),
        width = 3000,
        height = 70
        ))
        a.alignment = ft.alignment.center
        return a
    
    def grafics_card1(self):
        a = ft.Card(content = ft.Text('Зависимости от времени', text_align = ft.TextAlign.CENTER, size = 30), width = 4000, height = 55)
        return a

    
    def show_graphics(self):
        return ft.Column( controls = [
            self.grafics_card1(),
            self.grafics_card2(),
            ft.Row(controls=[self.graph_1,
                                self.graph_2,
                                self.graph_3])
        ])
    
    
    load_graphics = 0
    # 0 Не загружены
    # 1 Загружаются
    # 2 Загружены
    def analyze(self):

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Row(controls=[ft.ProgressRing(width=25, height=25, stroke_width = 2),ft.Text("Идёт загрузка...")]),
            content=ft.Row(controls = [ft.Text("Пожалуйста подождите, это займет не более минуты.")
            ]),
            actions_alignment=ft.MainAxisAlignment.END,
            open=True,
        )
        


        graphs = dlg_modal
        if self.graph_1 != None and self.graph_2 != None and self.graph_3 != None:
            graphs = self.show_graphics()
        else:
            if self.load_graphics == 0:
                self.load_graphics = 1


        controls = [
                self.topAppBar("Анализ и визуализация"),
                graphs,
                self.bottomAppBar(),
                self.sb,
                self.make_refresh()
            ]
    
        return controls

    def go_to_analyze(self, e):
        self.page.update()
        if self.active_button != 1:
            self.active_button = 1
            self.goto(self.analyze)
            
        self.page.update()

        if self.load_graphics == 1:
            print("Loading graphics")
            self.graphics()
            self.active_button = 1
            self.goto(self.analyze)

    # Prediction and GOTO prediction
        
   
        
    def predict_control(self):
        control = ft.Column(controls=[
            ft.ElevatedButton(text="Вызвать уведомление", on_click=self.notify_user)
        ])

        return control
    
    def predict_cards(self):
        control = ft.Card(content=ft.Row(controls=[
            ft.Icon(ft.icons.CALENDAR_MONTH_OUTLINED,color=ft.colors.PRIMARY, size=50),
            ft.Text('Выбранная дата: ' + str(self.current_date)[8:] +'.' +str(self.current_date)[5:7]+'.'+ str(self.current_date)[:4], text_align=ft.TextAlign.CENTER, size = 30)
        ],
        alignment=ft.MainAxisAlignment.CENTER
        ),width=4000, height=130)
        return control
    
    def prediction(self):
        normalColor = ft.colors.SURFACE_VARIANT
        normalTxtColor = ft.colors.PRIMARY
        regularButtonStyle = ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=0))
        hgt = self.bottomABhgt

        controls = [
                self.topAppBar("Прогнозирование"),
                self.predict_cards(),
                self.bottomAppBar(),
                self.sb,
                self.make_refresh(),
                ft.Row(controls = [
                ft.ElevatedButton(color=normalTxtColor,bgcolor=normalColor, icon=ft.icons.DATE_RANGE_OUTLINED, text="Предсказать на завтра",expand=True,height=hgt, style=ft.ButtonStyle(shape= ft.RoundedRectangleBorder(radius=20)),),
                ft.ElevatedButton(color=normalTxtColor, bgcolor=normalColor,icon=ft.icons.DATE_RANGE_OUTLINED, text="Предсказать на неделю", style=ft.ButtonStyle(shape= ft.RoundedRectangleBorder(radius=20)),expand=True,height=hgt),
                ft.ElevatedButton(color=normalTxtColor, bgcolor=normalColor, icon=ft.icons.DATE_RANGE_OUTLINED, text="Предсказать на месяц", style=ft.ButtonStyle(shape= ft.RoundedRectangleBorder(radius=20)), expand=True,height=hgt)])
                ]
        self.page.update()
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
        
    def check_if_user_exists(self,email):
        try:
            re = requests.request(url=self.webserver_url, method='GET', params={"email":email})
            response = str(re.content)[2:-1]
            if response == 'registered':
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
    # -2 - неверный формат данных email
    # -3 - неверный фонрмат данных password
    # -4 - пароли не совпадают
    # -5 - данный пользователь уже существует

    def email_change(self, e):
        self.email = str(e.control.value)
    def pass_change(self, e):
        self.password = str(e.control.value)

    def repeat_pass_change(self, e):
        self.repeat_password = str(e.control.value)

    def leave_register(self, e):
        self.is_registering = False
        self.email = ''
        self.password = ''
        self.repeat_password = ''
        self.goto(self.upload, True)

    def add_user(self, email, password, rpass):
        try:
            re = requests.request(url=self.webserver_url, method='GET', params={"email":email,"password":password, "rpassword":rpass})
            response = str(re.content)[2:-1]
            if response == 'success':
                return 1
            else:
                return 0
        except:
            return -1

    def do_register(self, e):
        if self.email == '' or self.password == '' or self.repeat_password == '':
            return
        e.control.disabled = True
        self.page.update()

        email = self.email
        password = self.password
        rpass = self.repeat_password

        print(email,password,rpass)

        if not ('@' in email and email.count('@') == 1):
            self.login_status = -2
            self.goto(self.upload)
        elif not (len(password) >= 8) or not (len(rpass) >= 8):
            self.login_status = -3
            self.goto(self.upload)
        elif not password == rpass:
            self.login_status = -4
            self.goto(self.upload)
        
        else:
            exists = self.check_if_user_exists(email)
            if exists:
                self.login_status = -5
                self.goto(self.upload)
            else:
                response = self.add_user(email,password,rpass)
                
                if response == 1:
                    self.login_status = 1
                    self.is_registering = False
                    self.goto(self.upload)
                else:
                    self.login_status = -1
                    self.goto(self.upload)

        e.control.disabled = False
        self.page.update()
    repeat_password = ''
    def register_form(self):

        base_color = ft.colors.PRIMARY_CONTAINER
        if self.d_or_l != 'dark':
            base_color = ft.colors.PRIMARY

        already_in = ft.Text(spans=[ft.TextSpan("Уже есть аккаунт?", on_click=self.leave_register, style=ft.TextStyle(color=ft.colors.PRIMARY,decoration=ft.TextDecoration.UNDERLINE))])


        txt = ft.Text(text_align=ft.TextAlign.CENTER,width=400)
        if self.login_status == -1:
            txt.value = "Сервер не отвечает, попробуйте позже."
            txt.color = ft.colors.RED
        elif self.login_status == 2:
            txt.value = "Неверный логин или пароль."
            txt.color = ft.colors.RED
        elif self.login_status == -2:
            txt.value = "Email введён некорректно"
            txt.color = ft.colors.RED
        elif self.login_status == -3:
            txt.value = "Пароль должен состоять минимум из 8 символов"
            txt.color = ft.colors.RED
        elif self.login_status == -4:
            txt.value = 'Пароли не совпадают'
            txt.color = ft.colors.RED
        elif self.login_status == -5:
            txt.value = "Пользователь уже зарегистрирован"
            txt.color = ft.colors.BLUE


        t1 = ft.TextField(label="Email",width=400,max_length=50, max_lines=1, on_change=self.email_change)
        t2 = ft.TextField(label="Пароль", width=400, max_length=50, max_lines=1, password=True, can_reveal_password=True,on_change=self.pass_change)
        t3 = ft.TextField(label="Повторите пароль", width=400, max_length=50, max_lines=1, password=True, can_reveal_password=True,on_change=self.repeat_pass_change)

        return ft.Row(controls=[
            ft.Column(controls=[
                t1,
                t2,
                t3,
                ft.Row(controls=[
                    ft.Column(controls=[
                        ft.ElevatedButton(color=ft.colors.WHITE, bgcolor=base_color, text="Зарегистрироваться", on_click=self.do_register, width=200),
                        already_in,
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

        register_text = ft.Text(spans=[ft.TextSpan("Зарегистрироваться", on_click=self.go_to_register, style=ft.TextStyle(color=ft.colors.PRIMARY,decoration=ft.TextDecoration.UNDERLINE))])
        
        t1 = ft.TextField(label="Email",width=400,max_length=50, max_lines=1, on_change=self.email_change)
        t2 = ft.TextField(label="Пароль", width=400, max_length=50, max_lines=1, password=True, can_reveal_password=True,on_change=self.pass_change)
        return ft.Row(controls=[
            ft.Column(controls=[
                t1,
                t2,
                ft.Row(controls=[
                    ft.Column(controls=[
                        ft.ElevatedButton(color=ft.colors.WHITE, bgcolor=base_color, text="Войти", on_click=self.login, width=100),
                        register_text,
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
            re = requests.request(url=self.webserver_url, method="post", files=nfiles, params={"email":self.email,"password":self.password})
            if re.content == 'failed':
                self.email = ''
                self.password = ''
                print("Неверный логин или пароль")
                self.login_status = 2
                self.goto(self.upload)
            else:
                print("Выкладывание файлов")
        elif url != None:
            return
        
        re.content
        
        self.file_picker_button.disabled = False
        self.file_upload_button.disabled = False
        self.page.update()

    def upload_form(self):
        tp = ft.TextField(label='URL', width=600,max_lines=1,on_change=self.get_file_from_url)
        your_files = None
        txt = ft.Text("Здесь пусто")
        return ft.Column(controls=[
                self.file_picker_button,
                ft.Divider(),
                ft.Row(controls=[
                    tp,
                    self.file_upload_button
                ],
                width=810,
                spacing=10,
                ),
                
                ft.Divider(),
                ft.Text("Ваши файлы:"),
                txt
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=810
            )
            
        
        
    def upload(self):


        form = self.login_form()

    
        if self.is_registering == True:
            form = self.register_form()

        if self.login_status == 1:
            form = self.upload_form()

        
        controls = [
                self.topAppBar("Загрузка файлов"),
                form,

                self.bottomAppBar(),
                self.sb,
                self.make_refresh()
            ]
        return controls

    def go_to_upload(self, e):
        self.page.update()
        if self.active_button != 3:
            self.active_button = 3
            self.goto(self.upload)
        self.page.update()


    

    def goto(self, where, clear:bool=False):
        if self.login_status != 1 and clear:
            self.login_status = 0
            self.email = ''
            self.password = ''
            self.repeat_password = ''
        self.page.views.clear()
        self.page.views.append(
            View(
                "/",
                where()
        ))
        self.sb.open = False
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
                func(),
                self.sb
        ))
        self.sb.open = False

        self.page.update()