import flet as ft
import time
from datetime import datetime
from decimal import *
# now for the main class for the charts


class TimeDoubleChart(ft.UserControl):
    def __init__(self, vtext: str, data1: list | dict, coin: bool, predeterminado: str | None = None):
        # instances for the chart
        self.coin = coin
        self.actual_month = 'Septiembre'
        self.actual_month2 = 'Septiembre'
        if isinstance(data1, list):
            self.country_data = data1
            self.dic_data = None
        else:
            self.dic_data = data1
            self.get_data_points_state(predeterminado)

        self.data_points_1: list = []
        self.data_points_2: list = []
        self.data_points_3: list = []

        self.data_points2_1: list = []
        self.data_points2_2: list = []
        self.data_points2_3: list = []
        # metodo que estructura las listas bien
        self.get_data_points_month(self.actual_month)
        self.get_data_points_month2(self.actual_month2)
        # some instances
        self.data_points: list = []
        self.data_points2: list = []
        self.points: list = self.data_points_1
        self.points2: list = self.data_points2_1  # start off with the gold prices frist
        # text instance
        self.text = ft.Text(
                    vtext,
                    size=16,
                    weight='bold'
                )
        # chart instance
        self.chart: ft.Control = ft.LineChart(
            # tooltip is the display price upon hovering
            tooltip_bgcolor=ft.colors.with_opacity(0.75, ft.colors.WHITE),
            expand=True,
            # we'll be using the min and max built-in function to get the min/
            # max of x and y
            # wrap it all in an int, so we avoid fractions
            min_y=float(min((self.points + self.points2), key=lambda y: y[1])[1]),
            max_y=float(max((self.points + self.points2), key=lambda y: y[1])[1]),
            min_x=float(min((self.points + self.points2), key=lambda x: x[0])[0]),
            max_x=float(max((self.points + self.points2), key=lambda x: x[0])[0]),
            # finally the axis labels
            left_axis=ft.ChartAxis(
                labels_size=50,
            ),
            bottom_axis=ft.ChartAxis(
                labels_size=40,
                labels_interval=1
            ),
        )
        # the properties of the line/curve
        self.line_chart: ft.Control = ft.LineChartData(
                color=ft.colors.GREEN,
                stroke_width=2,
                curved=True,
                stroke_cap_round=True,
                below_line_gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.colors.with_opacity(0.25, ft.colors.GREEN), "transparent"],
                    )
                )

        self.line_chart2: ft.Control = ft.LineChartData(
                color=ft.colors.RED,
                stroke_width=2,
                curved=True,
                stroke_cap_round=True,
                below_line_gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.colors.with_opacity(0.25, ft.colors.RED), "transparent"],
                )
            )

        super().__init__()

    # we need two buttons to toggle between the two data sets
    def get_data_buttons(self, icon_name, btn_name, data):
        return ft.ElevatedButton(
            btn_name,
            color='white',
            icon=icon_name,
            width=140,
            height=50,
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=6)},
            ),
            bgcolor='teal600',
            data=data,
            on_click=lambda e: self.toggle_data(e)
        )

    def get_data_points_month(self, month: str):
        self.actual_month = month
        mes = 0
        match month:
            case 'Enero':
                mes = 1
            case 'Febrero':
                mes = 2
            case 'Marzo':
                mes = 3
            case 'Abril':
                mes = 4
            case 'Mayo':
                mes = 5
            case 'Junio':
                mes = 6
            case 'Julio':
                mes = 7
            case 'Agosto':
                mes = 8
            case 'Septiembre':
                mes = 9
        self.data_points_1 = []
        self.data_points_2 = []
        self.data_points_3 = []

        for item in self.country_data[0]:
            date_month = datetime.strptime(item[0], '%Y-%m-%d')
            if date_month.month == mes:
                self.data_points_1.append((date_month.day, float(item[1])))
        for item in self.country_data[1]:
            date_month = datetime.strptime(item[0], '%Y-%m-%d')
            if date_month.month == mes:
                self.data_points_2.append((date_month.day, float(item[1])))
        for item in self.country_data[2]:
            date_month = datetime.strptime(item[0], '%Y-%m-%d')
            if date_month.month == mes:
                self.data_points_3.append((date_month.day, float(item[1])))

    def get_data_points_month2(self, month: str):
        self.actual_month2 = month
        mes = 0
        match month:
            case 'Enero':
                mes = 1
            case 'Febrero':
                mes = 2
            case 'Marzo':
                mes = 3
            case 'Abril':
                mes = 4
            case 'Mayo':
                mes = 5
            case 'Junio':
                mes = 6
            case 'Julio':
                mes = 7
            case 'Agosto':
                mes = 8
            case 'Septiembre':
                mes = 9
        self.data_points2_1 = []
        self.data_points2_2 = []
        self.data_points2_3 = []

        for item in self.country_data[0]:
            date_month = datetime.strptime(item[0], '%Y-%m-%d')
            if date_month.month == mes:
                self.data_points2_1.append((date_month.day, float(item[1])))
        for item in self.country_data[1]:
            date_month = datetime.strptime(item[0], '%Y-%m-%d')
            if date_month.month == mes:
                self.data_points2_2.append((date_month.day, float(item[1])))
        for item in self.country_data[2]:
            date_month = datetime.strptime(item[0], '%Y-%m-%d')
            if date_month.month == mes:
                self.data_points2_3.append((date_month.day, float(item[1])))

    def toggle_dropdown(self, e):
        if e.control.data == 'month1':
            self.toggle_month(e)
        elif e.control.data == 'month2':
            self.toggle_month2(e)
        elif e.control.data == 'state':
            self.toogle_state(e)

    def get_data_points_state(self, state: str):
        self.country_data = self.dic_data[state]

    def toogle_state(self, e):
        self.get_data_points_state(e.data)
        self.get_data_points_month(self.actual_month)
        self.get_data_points_month2(self.actual_month2)
        self.points = self.data_points_1
        self.points2 = self.data_points2_1
        # after setting the data points list, we need reset the chart
        self.data_points = []
        self.data_points2 = []
        self.chart.data_series = []
        self.line_chart.data_points = self.data_points
        self.line_chart2.data_points = self.data_points2

        # we need to reset the axis values as well
        self.chart.min_y = float(min((self.points + self.points2), key=lambda y: y[1])[1])
        self.chart.max_y = float(max((self.points + self.points2), key=lambda y: y[1])[1])
        self.chart.min_x = float(min((self.points + self.points2), key=lambda x: x[0])[0])
        self.chart.max_x = float(max((self.points + self.points2), key=lambda x: x[0])[0])

        self.chart.update()
        time.sleep(0.5)

        # next re-insert the line chart into the self.chart instance
        self.chart.data_series = [self.line_chart, self.line_chart2]
        # and finally, call the method below to get the new data points
        self.get_data_points()

    def get_data_buttons_dropdown(self, label: str, options: list, value: str, data: str, color: str):
        return ft.Dropdown(
            label=label,
            width=140,
            height=50,
            text_size=14,
            color='white',
            border_color=color,
            filled=True,
            bgcolor='teal600',
            border_radius=6,
            label_style=ft.TextStyle(
                color='white',
            ),
            options=options,
            value=value,
            autofocus=True,
            data=data,
            on_change=lambda e: self.toggle_dropdown(e),
            # icon=icon_name,
        )

    # now, we need a way to toggle between each set while resseting the chart
    # along the way
    def toggle_month(self, e):
        self.get_data_points_month(e.data)
        self.points = self.data_points_1
        self.points2 = self.data_points2_1
        # after setting the data points list, we need reset the chart
        self.data_points = []
        self.data_points2 = []
        self.chart.data_series = []
        self.line_chart.data_points = self.data_points
        self.line_chart2.data_points = self.data_points2

        # we need to reset the axis values as well
        self.chart.min_y = float(min((self.points + self.points2), key=lambda y: y[1])[1])
        self.chart.max_y = float(max((self.points + self.points2), key=lambda y: y[1])[1])
        self.chart.min_x = float(min((self.points + self.points2), key=lambda x: x[0])[0])
        self.chart.max_x = float(max((self.points + self.points2), key=lambda x: x[0])[0])

        self.chart.update()
        time.sleep(0.5)

        # next re-insert the line chart into the self.chart instance
        self.chart.data_series = [self.line_chart, self.line_chart2]
        # and finally, call the method below to get the new data points
        self.get_data_points()

    def toggle_month2(self, e):
        self.get_data_points_month2(e.data)
        self.points = self.data_points_1
        self.points2 = self.data_points2_1
        # after setting the data points list, we need reset the chart
        self.data_points = []
        self.data_points2 = []
        self.chart.data_series = []
        self.line_chart.data_points = self.data_points
        self.line_chart2.data_points = self.data_points2

        # we need to reset the axis values as well
        self.chart.min_y = float(min((self.points + self.points2), key=lambda y: y[1])[1])
        self.chart.max_y = float(max((self.points + self.points2), key=lambda y: y[1])[1])
        self.chart.min_x = float(min((self.points + self.points2), key=lambda x: x[0])[0])
        self.chart.max_x = float(max((self.points + self.points2), key=lambda x: x[0])[0])

        self.chart.update()
        time.sleep(0.5)

        # next re-insert the line chart into the self.chart instance
        self.chart.data_series = [self.line_chart, self.line_chart2]
        # and finally, call the method below to get the new data points
        self.get_data_points()

    def toggle_data(self, e):
        self.switch_list(e)

        # next re-insert the line chart into the self.chart instance
        self.chart.data_series = [self.line_chart, self.line_chart2]

        # and finally, call the method below to get the new data points
        self.get_data_points()

    def switch_list(self, e):
        # print(e.control.data)
        if self.coin:
            if e.control.data == 'd1':
                self.points = self.data_points_1
                self.points2 = self.data_points2_1
                self.text.value = "Cambios de moneda por mes de DOLAR"
            if e.control.data == 'd2':
                self.points = self.data_points_2
                self.points2 = self.data_points2_2
                self.text.value = 'Cambios de moneda por mes de EURO'
            if e.control.data == 'd3':
                self.points = self.data_points_3
                self.points2 = self.data_points2_3
                self.text.value = 'Cambios de moneda por mes de QUETZAL'
        else:
            if e.control.data == 'd1':
                self.points = self.data_points_1
                self.text.value = "'Cambios de clima por mes y depertamento (MINIMO)'"
            if e.control.data == 'd2':
                self.points = self.data_points_2
                self.text.value = 'Cambios de clima por mes y depertamento (PROMEDIO)'
            if e.control.data == 'd3':
                self.points = self.data_points_3
                self.text.value = 'Cambios de clima por mes y depertamento (MAXIMO)'
        # after setting the data points list, we need reset the chart
        self.data_points = []
        self.data_points2 = []
        self.chart.data_series = []
        self.line_chart.data_points = self.data_points
        self.line_chart2.data_points = self.data_points2

        # we need to reset the axis values as well
        self.chart.min_y = float(min((self.points + self.points2), key=lambda y: y[1])[1])
        self.chart.max_y = float(max((self.points + self.points2), key=lambda y: y[1])[1])
        self.chart.min_x = float(min((self.points + self.points2), key=lambda x: x[0])[0])
        self.chart.max_x = float(max((self.points + self.points2), key=lambda x: x[0])[0])

        self.chart.update()
        self.text.update()
        time.sleep(0.5)

    # method to create the data points for the line chart
    def create_data_point(self, x, y):
        return ft.LineChartDataPoint(
            x,
            y,
            # this property is for the annotated point when hovered, the white
            # dashed line underneath each price point
            selected_below_line=ft.ChartPointLine(
                width=0.5,
                color='white54',
                dash_pattern=[2, 4],
            ),
            selected_point=ft.ChartCirclePoint(
                stroke_width=1
            ),
        )
    # method to make a list of the above method
    def get_data_points(self):
        for x, y, in self.points:
            self.data_points.append(self.create_data_point(x, y))
            self.chart.update()
            time.sleep(0.05)

        for x, y, in self.points2:
            self.data_points2.append(self.create_data_point(x, y))
            self.chart.update()
            time.sleep(0.05)

    def build(self):
        self.line_chart.data_points = self.data_points
        self.line_chart2.data_points = self.data_points2
        self.chart.data_series = [self.line_chart, self.line_chart2]

        return ft.Column(
            horizontal_alignment='center',
            controls=[
                self.text,
                self.chart,
            ],
        )
