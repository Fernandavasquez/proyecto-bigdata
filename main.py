import flet
from flet import *
from functools import partial
import time

import mysqldb
from chart import TimeChart
from mongodb import MongoDB
from dynamodb import DynamoDB


class ModernNavBar(UserControl):
    def __init__(self, func, pais, moneda, comparar_moneda, clima, comparar_clima, clima_moneda, analisis, db):
        self.func = func
        self.button_pais = pais
        self.button_moneda = moneda
        self.button_comparar_moneda = comparar_moneda
        self.button_clima = clima
        self.button_comparar_clima = comparar_clima
        self.button_clima_moneda = clima_moneda
        self.button_analisis = analisis
        self.button_db = db
        super().__init__()

    # we want to highlight the specific row whenever we
    # hover over the icons

    def highlight(self, e):
        if e.data == 'true':
            if not e.control.bgcolor == 'white24':
                e.control.bgcolor = 'white10'
                e.control.update()

                # I want to also make the highlighted turn white
                # to delinate the color from the rest of the icons

                e.control.content.controls[0].icon_color = 'white'
                # the .controls[0] and .controls[1] refere to control index
                # position i.e. for the IconButton and the Text
                e.control.content.controls[1].color = 'white'
                e.control.content.update()
        else:
            if e.control.bgcolor == 'white10':
                e.control.bgcolor = None
                e.control.update()

                # I want to also make the highlighted turn white
                # to delinate the color from the rest of the icons

                e.control.content.controls[0].icon_color = 'white54'
                # the .controls[0] and .controls[1] refere to control index
                # position i.e. for the IconButton and the Text
                e.control.content.controls[1].color = 'white54'
                e.control.content.update()

    def user_data(self, initials: str, name: str, description: str):
        # first row has user info, diferrent from the icon rows,
        # so we create a separate function for it
        return Container(
            content=Row(
                controls=[
                    Container(
                        width=52,
                        height=52,
                        bgcolor='bluegrey900',
                        alignment=alignment.center,
                        border_radius=10,
                        content=Text(
                            value=initials,  # pass args below
                            size=25,
                            weight='bold',
                        ),
                    ),
                    Column(
                        spacing=1,
                        alignment=alignment.center,
                        controls=[
                            Text(
                                value=name,
                                size=18,
                                weight='bold',
                                # Here we nedd to include some details
                                # for de animation icones later
                                opacity=1,  # full opaciti 0-1
                                animate_opacity=200  # speed of animation
                            ),
                            Text(
                                value=description,
                                size=14,
                                weight='w400',
                                color='white54',
                                # Here we nedd to include some details
                                # for de animation icones later
                                opacity=1,  # full opaciti 0-1
                                animate_opacity=200  # speed of animation
                            ),
                        ]
                    )
                ]
            )
        )

    # now for the main sidebar row and icons
    def contained_icon(self, icon_name: str, text: str, funct):
        return Container(
            width=230,
            height=48,
            border_radius=10,
            on_hover=lambda e: self.highlight(e),
            on_click=partial(funct),
            content=Row(
                controls=[
                    IconButton(
                        icon=icon_name,
                        icon_size=30,
                        icon_color='white54',
                        style=ButtonStyle(
                            shape={
                                "": RoundedRectangleBorder(radius=7),
                            },
                            overlay_color={
                                "": 'transparent'
                            }
                        ),
                    ),
                    Text(
                        value=text,
                        color='white54',
                        size=18,
                        opacity=1,
                        animate_opacity=200,
                    )
                ]
            ),
        )

    def contained_icon_dropdown(self, icon_name: str, text: str, funct):
        return Container(
            padding=padding.only(top=5),
            width=230,
            height=58,
            border_radius=10,
            #on_hover=lambda e: self.highlight(e),
            content=Row(
                controls=[
                    Dropdown(
                        label=text,
                        width=220,
                        text_size=13,
                        border_radius=6,
                        border_color='white',
                        label_style=TextStyle(
                            color='white'
                        ),
                        color='white',
                        options=[
                            dropdown.Option("MySQL"),
                            dropdown.Option("MongoDB"),
                            dropdown.Option("DynamoDB"),
                        ],
                        value='MongoDB',
                        autofocus=True,
                        on_change=partial(funct),
                        icon=icon_name,
                    )
                ]
            ),
        )

    def build(self):
        return Container(
            # defube tge dimensions and characteristics
            # of the returned container
            width=250,
            height=680,
            alignment=alignment.center,
            content=Column(
                alignment=MainAxisAlignment.START,
                horizontal_alignment="center",
                controls=[
                    # here I'll have a small clickable container
                    # to minimaze and expand the sidebar => this can be
                    # anything (button, etc...)
                    Container(
                        width=230,
                        height=48,
                        border_radius=8,
                        bgcolor=colors.with_opacity(0.2, 'grey'),
                        alignment=alignment.center_right,
                        on_click=partial(self.func),  # we pass a partial
                        # function here, so we can pass in the animation
                        # method in the main function below
                        content=IconButton(
                            icon=icons.CHEVRON_LEFT,
                            icon_size=30,
                            icon_color='white',
                            style=ButtonStyle(
                                shape={
                                    "": RoundedRectangleBorder(radius=7),
                                },
                                overlay_color={
                                    "": 'transparent'
                                }
                            ),

                        )
                    ),
                    # add the sidebar icons here...
                    self.user_data('CS', 'Cristian Siguenza', 'Software Engineer'),
                    # add a divider

                    Divider(height=5, color='transparent'),
                    self.contained_icon(icons.SEARCH, "Pais", self.button_pais),
                    self.contained_icon(icons.DATA_EXPLORATION_OUTLINED, "Moneda", self.button_moneda),
                    self.contained_icon(icons.BAR_CHART, "Comparar moneda", self.button_comparar_moneda),
                    self.contained_icon(icons.CLOUDY_SNOWING, "Clima", self.button_clima),
                    self.contained_icon(icons.PIE_CHART_ROUNDED, "Comparar clima", self.button_comparar_clima),
                    self.contained_icon(icons.MULTILINE_CHART_ROUNDED, "Clima-Moneda", self.button_clima_moneda),
                    self.contained_icon(icons.ANALYTICS_OUTLINED, "Analisis", self.button_analisis),
                    Divider(height=5, color='white54'),
                    self.contained_icon_dropdown(icons.DNS_ROUNDED, "Base de datos", self.button_db),
                ]
            ),
        )


def main(page: Page):
    mongo = MongoDB()
    # title
    page.title = 'Flet Modern Sidebar'
    # page width and height
    page.window_height = 750
    page.window_width = 1250
    page.window_min_height = 750
    page.window_min_width = 1250
    page.window_max_height = 750
    page.window_max_width = 1250
    page.window_center()
    page.window_maximizable = False
    # alignements
    page.horizontal_alignment = 'top-left'
    page.vertical_alignment = 'top-left'

    # animate sidebar

    def animate_sidebar(e):
        # there are several steps to animate the sidebar
        # first, we check if the width is at the desired end width,
        # page.controls[0] is the class we called. The class is at the
        # controls[0] position and recall that the class returns the
        # container that we will minimze and expand
        if page.controls[0].controls[0].width != 72:
            # since the sidebar(i.e., container) is no 62,
            # this if statement will run.
            # so we need to first reduce the opasity before minimizing

            # reducing opacity of title text
            for item in (
                    # we need to iterate through the rows and icons that
                    # were returnered by the class ModernNavBar
                    # so the class is at this position:
                    page.controls[0].controls[0]
                            # next is the content of the container
                            .content.controls[0]
                            # next is the row controls
                            .content.controls[1]
                            # another layer here (!)
                            .content.controls[1]
                            # then the position of the text (:) means the entire list of controls
                            .controls[:]
            ):
                item.opacity = 0  # so each item now refers to the Text() control in the Sidebar
                item.update()

            # reducing opacity of the sidebar menu items
            cont = 3
            for items in page.controls[0].controls[0].content.controls[0].content.controls[3:]:
                if isinstance(items, Container):
                    cont += 1
                    if cont < 11:
                        items.content.controls[1].opacity = 0
                        items.content.update()
                    else:
                        items.content.controls[0].opacity = 0
                        items.content.update()

            # sleep
            time.sleep(0.2)

            # finally minimze the sidebar container sizze
            page.controls[0].controls[0].width = 72
            page.controls[0].controls[1].width = 1128
            page.controls[0].update()

            page.controls[0].controls[0].content.controls[0].content.controls[0].content.icon = icons.CHEVRON_RIGHT
            page.controls[0].controls[0].content.controls[0].content.controls[0].content.update()

        # now we do the opposite
        else:
            page.controls[0].controls[0].width = 250
            page.controls[0].controls[1].width = 950
            page.controls[0].update()
            time.sleep(0.2)

            page.controls[0].controls[0].content.controls[0].content.controls[0].content.icon = icons.CHEVRON_LEFT
            page.controls[0].controls[0].content.controls[0].content.controls[0].content.update()

            for item in (page.controls[0].controls[0].content.controls[0].content.controls[1].content.controls[1].controls[:]):
                item.opacity = 1
                item.update()
            cont = 3
            for items in page.controls[0].controls[0].content.controls[0].content.controls[3:]:
                if isinstance(items, Container):
                    cont += 1
                    if cont < 11:
                        items.content.controls[1].opacity = 1
                        items.content.update()
                    else:
                        items.content.controls[0].opacity = 1
                        items.content.update()


    txt_pais = TextField(
        label="Buscar pais",
        text_size=20,
        text_style=TextStyle(
            color='White'
        ),
        border=InputBorder.UNDERLINE,
        border_color=colors.GREEN_ACCENT,
        hint_text="Ingrese el pais.",
    )

    text_states = Text(
        width=250,
        height=180,
        size=75,
        color='white',
        weight='bold',
        text_align=TextAlign.CENTER,
    )
    text_currencies = Text(
        width=250,
        height=180,
        size=75,
        color='white',
        weight='bold',
        text_align=TextAlign.CENTER,
    )
    text_datacoin = Text(
        value='167',
        width=250,
        height=180,
        size=75,
        color='white',
        weight='bold',
        text_align=TextAlign.CENTER,
    )

    text_dataweather = Text(
        value='167',
        width=250,
        height=180,
        size=75,
        color='white',
        weight='bold',
        text_align=TextAlign.CENTER,
    )

    text_shortname = Text(
        width=250,
        height=180,
        size=75,
        color='white',
        weight='bold',
        text_align=TextAlign.CENTER,
    )

    text_capital = Text(
        width=250,
        height=180,
        size=40,
        color='white',
        weight='bold',
        text_align=TextAlign.CENTER,
    )

    def submit_textfield_pais(e):
        global country_weather
        global country_coin
        if database == 'MySQL':
            response = mysqldb.query_MysqlCountry(txt_pais.value)
            print(response[0][1])
            if response is not None:
                text_states.value = str(mysqldb.query_dataestados(response[0][1]))
                text_currencies.value = str(response[0][2])
                text_shortname.value = str(response[0][1])
                text_capital.value = str(response[0][3]).upper()
                #query for the coin data
                aux1 = []
                coin_gtq, coin_usd, coin_eur, coin_base = mysqldb.query_dataCC(response[0][1])
                aux1.append(coin_gtq)
                aux1.append(coin_usd)
                aux1.append(coin_eur)
                aux1.append(coin_base)
                country_coin = aux1
                # query for the weather data.
                country_weather = mysqldb.query_dataWeather(response[0])
        elif database == 'MongoDB':
            response = mongo.query_data_c({'name': txt_pais.value})
            if response is not None:
                text_states.value = str(len(response['states']))
                text_currencies.value = str(response['currencies'][0])
                text_shortname.value = str(response['country_id'])
                text_capital.value = str(response['capital']).upper()

                aux = []
                coin_gtq, coin_usd, coin_eur, coin_base = mongo.query_data_countrycoin({'country_id': response['country_id']})
                aux.append(coin_gtq)
                aux.append(coin_usd)
                aux.append(coin_eur)
                aux.append(coin_base)
                country_coin = aux

                country_weather = mongo.query_data_countryweather({'country_id': response['country_id']})

        elif database == 'DynamoDB':
            pass

        page.update()

    chart_container = Container(
        width=950,
        height=680,
        bgcolor=colors.with_opacity(0.5, 'black'),
        animate=animation.Animation(500, 'decelerate'),
        alignment=alignment.center,
        border_radius=10,
        padding=10,
        content=Text("BIENVENIDO...\n              by FCPC", color='white', weight='bold', size=30, animate_opacity=200)
    )

    def clean_selected_color():
        for items in page.controls[0].controls[0].content.controls[0].content.controls[3:10]:
            if isinstance(items, Container):
                items.content.controls[1].color = 'white54'
                items.content.controls[0].icon_color = 'white54'
                items.bgcolor = None
                items.update()

    # buttons functions
    def button_pais(e):
        clean_selected_color()

        page.controls[0].controls[0].content.controls[0].content.controls[3].bgcolor = 'white24'
        page.controls[0].controls[0].content.controls[0].content.controls[3].content.controls[1].color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[3].content.controls[0].icon_color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[3].update()
        chart_container.clean()
        chart_container.content = Column(
            expand=True,
            alignment='center',
            horizontal_alignment='center',
            controls=[
                Container(
                    expand=1,
                    border_radius=6,
                    bgcolor=colors.with_opacity(0.05, colors.WHITE10),
                    content=Row(
                        alignment='center',
                        controls=[
                            txt_pais,
                            ElevatedButton(
                                color=colors.GREEN_ACCENT,
                                bgcolor='white10',
                                icon=icons.SEARCH,
                                icon_color=colors.GREEN_ACCENT,
                                text="Buscar",
                                on_click=lambda es: submit_textfield_pais(es),
                                ),
                        ]
                    )
                ),
                Row(
                    height=270,
                    controls=[
                        Container(
                            expand=1,
                            height=250,
                            width=250,
                            border_radius=6,
                            bgcolor=colors.with_opacity(0.05, colors.WHITE10),
                            content=Column(
                                controls=[
                                    Text('ESTADOS:',
                                         color=colors.GREEN_ACCENT,
                                         weight='bold',
                                         size=24),
                                    text_states,
                                ]
                            ),
                            padding=20,
                        ),
                        Container(
                            expand=1,
                            height=250,
                            width=250,
                            border_radius=6,
                            bgcolor=colors.with_opacity(0.05, colors.WHITE10),
                            content=Column(
                                controls=[
                                    Text('DATOS TOTALES SOBRE MONEDA:',
                                         color=colors.GREEN_ACCENT,
                                         weight='bold',
                                         size=24),
                                    text_datacoin,
                                ]
                            ),
                            padding=20,
                        ),
                        Container(
                            expand=1,
                            height=250,
                            width=250,
                            border_radius=6,
                            bgcolor=colors.with_opacity(0.05, colors.WHITE10),
                            content=Column(
                                controls=[
                                    Text('DATOS TOTALES SOBRE CLIMA:',
                                         color=colors.GREEN_ACCENT,
                                         weight='bold',
                                         size=24),
                                    text_dataweather,
                                ]
                            ),
                            padding=20,
                        ),
                    ]
                ),
                Row(
                    height=270,
                    controls=[
                        Container(
                            expand=1,
                            height=250,
                            width=250,
                            border_radius=6,
                            bgcolor=colors.with_opacity(0.05, colors.WHITE10),
                            content=Column(
                                controls=[
                                    Text('ABREVIATURA:',
                                         color=colors.GREEN_ACCENT,
                                         weight='bold',
                                         size=24),
                                    text_shortname,
                                ]
                            ),
                            padding=20,
                        ),
                        Container(
                            expand=1,
                            height=250,
                            width=250,
                            border_radius=6,
                            bgcolor=colors.with_opacity(0.05, colors.WHITE10),
                            content=Column(
                                controls=[
                                    Text('SIMBOLO DE MONEDA:',
                                         color=colors.GREEN_ACCENT,
                                         weight='bold',
                                         size=24),
                                    text_currencies,
                                ]
                            ),
                            padding=20,
                        ),
                        Container(
                            expand=1,
                            height=250,
                            width=250,
                            border_radius=6,
                            bgcolor=colors.with_opacity(0.05, colors.WHITE10),
                            content=Column(
                                controls=[
                                    Text('CAPITAL:',
                                         color=colors.GREEN_ACCENT,
                                         weight='bold',
                                         size=24),
                                    text_capital,
                                ]
                            ),
                            padding=20,
                        ),
                    ]
                ),
            ]
        )
        page.update()
        chart_container.update()

    def button_moneda(e):
        clean_selected_color()

        opciones_mes = [
            dropdown.Option("Enero"),
            dropdown.Option("Febrero"),
            dropdown.Option("Marzo"),
            dropdown.Option("Abril"),
            dropdown.Option("Mayo"),
            dropdown.Option("Junio"),
            dropdown.Option("Julio"),
            dropdown.Option("Agosto"),
            dropdown.Option("Septiembre"),
        ]

        page.controls[0].controls[0].content.controls[0].content.controls[4].bgcolor = 'white24'
        page.controls[0].controls[0].content.controls[0].content.controls[4].content.controls[1].color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[4].content.controls[0].icon_color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[4].update()
        chart_container.clean()
        chart = TimeChart('Cambios de moneda por mes de DOLAR', country_coin, True)
        chart_container.content = Column(
            expand=True,
            alignment='center',
            horizontal_alignment='center',
            controls=[
                Container(
                    expand=1,
                    border_radius=6,
                    bgcolor=colors.with_opacity(0.05, colors.WHITE10),
                    content=Row(
                        alignment='center',
                        controls=[
                            chart.get_data_buttons(icons.ATTACH_MONEY, "Dolar", 'd1'),
                            chart.get_data_buttons(icons.EURO_SYMBOL, "Euro", 'd2'),
                            chart.get_data_buttons(icons.QUORA, "Quetzal", 'd3'),
                            chart.get_data_buttons_dropdown('Seleccionar mes', opciones_mes, 'Septiembre', 'month'),
                        ]
                    )
                ),
                Container(
                    expand=4,
                    border_radius=6,
                    bgcolor=colors.with_opacity(0.05, colors.WHITE10),
                    content=chart,
                    padding=20,
                )
            ]
        )
        chart_container.update()
        # run the method of get data points
        time.sleep(1)
        chart.get_data_points()

    def button_comparar_moneda(e):
        clean_selected_color()

        page.controls[0].controls[0].content.controls[0].content.controls[5].bgcolor = 'white24'
        page.controls[0].controls[0].content.controls[0].content.controls[5].content.controls[1].color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[5].content.controls[0].icon_color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[5].update()
        chart_container.content = Text("CLICKED IN COMPARE COIN", color='white', weight='bold', size=18, animate_opacity=200)
        chart_container.update()

    def button_clima(e):
        clean_selected_color()
        opciones_mes = [
                dropdown.Option("Enero"),
                dropdown.Option("Febrero"),
                dropdown.Option("Marzo"),
                dropdown.Option("Abril"),
                dropdown.Option("Mayo"),
                dropdown.Option("Junio"),
                dropdown.Option("Julio"),
                dropdown.Option("Agosto"),
                dropdown.Option("Septiembre"),
            ]
        opciones_estados = []
        predetrminado: str = ''
        for key in country_weather.keys():
            predetrminado = str(key)
            opciones_estados.append(dropdown.Option(str(key)))

        page.controls[0].controls[0].content.controls[0].content.controls[4].bgcolor = 'white24'
        page.controls[0].controls[0].content.controls[0].content.controls[4].content.controls[1].color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[4].content.controls[0].icon_color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[4].update()
        chart_container.clean()
        chart = TimeChart('Cambios de clima por mes y depertamento (MINIMO)', country_weather, False, predetrminado)
        chart_container.content = Column(
            expand=True,
            alignment='center',
            horizontal_alignment='center',
            controls=[
                Container(
                    expand=1,
                    border_radius=6,
                    bgcolor=colors.with_opacity(0.05, colors.WHITE10),
                    content=Row(
                        alignment='center',
                        controls=[
                            chart.get_data_buttons_dropdown('Seleccionar estado', opciones_estados, predetrminado, 'state'),
                            chart.get_data_buttons(icons.SEVERE_COLD_SHARP, "Minimo", 'd1'),
                            chart.get_data_buttons(icons.THERMOSTAT, "Promedio", 'd2'),
                            chart.get_data_buttons(icons.WHATSHOT_SHARP, "Maximo", 'd3'),
                            chart.get_data_buttons_dropdown('Seleccionar mes', opciones_mes, 'Septiembre', 'month'),
                        ]
                    )
                ),
                Container(
                    expand=4,
                    border_radius=6,
                    bgcolor=colors.with_opacity(0.05, colors.WHITE10),
                    content=chart,
                    padding=20,
                )
            ]
        )
        chart_container.update()
        # run the method of get data points
        time.sleep(1)
        chart.get_data_points()

    def button_comparar_clima(e):
        clean_selected_color()

        page.controls[0].controls[0].content.controls[0].content.controls[7].bgcolor = 'white24'
        page.controls[0].controls[0].content.controls[0].content.controls[7].content.controls[1].color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[7].content.controls[0].icon_color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[7].update()
        chart_container.content = Text("CLICKED IN COMPARE WEATHER ", color='white', weight='bold', size=18, animate_opacity=200)
        chart_container.update()

    def button_clima_moneda(e):
        clean_selected_color()

        page.controls[0].controls[0].content.controls[0].content.controls[8].bgcolor = 'white24'
        page.controls[0].controls[0].content.controls[0].content.controls[8].content.controls[1].color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[8].content.controls[0].icon_color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[8].update()
        chart_container.content = Text("CLICKED IN WEATHER-COIN", color='white', weight='bold', size=18, animate_opacity=200)
        chart_container.update()

    def button_analisis(e):
        clean_selected_color()

        page.controls[0].controls[0].content.controls[0].content.controls[9].bgcolor = 'white24'
        page.controls[0].controls[0].content.controls[0].content.controls[9].content.controls[1].color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[9].content.controls[0].icon_color = 'white'
        page.controls[0].controls[0].content.controls[0].content.controls[9].update()
        chart_container.content = Text("CLICKED IN ANALYTICS", color='white', size=18, opacity=1, animate_opacity=200)
        chart_container.update()

    def button_bd(e):
        global database
        database = 'MongoDB'
        clean_selected_color()
        database = str(e.data)

    # add class to page
    page.add(
        Row(
            alignment=MainAxisAlignment.START,
            width=1200,
            height=700,
            controls=[
                Container(
                    width=250,
                    height=680,
                    bgcolor='black',
                    border_radius=10,
                    animate=animation.Animation(500, 'decelerate'),
                    alignment=alignment.center,
                    padding=10,
                    content=ModernNavBar(animate_sidebar, button_pais, button_moneda, button_comparar_moneda,
                                         button_clima, button_comparar_clima, button_clima_moneda, button_analisis,
                                         button_bd),
                ),
                chart_container,
            ],
            expand=True,
        )
    )
    page.update()


# run
if __name__ == '__main__':
    flet.app(target=main)
