import flet as ft
import time

GOLD: list = [
    (0, 273.60),
    (1, 279.00),
    (2, 348.20),
    (3, 363.70),
    (4, 438.40),
    (5, 518.90),
    (6, 638.00),
    (7, 833.75),
    (8, 874.75),
    (9, 1096.50),
    (10, 1226.75),
    (11, 1577.00),
    (12, 1668.75),
    (13, 1200.00),
    (14, 1184.75),
    (15, 1061.25),
    (16, 1151.00),
    (17, 1257.25),
    (18, 1301.50),
    (19, 1493.25),
    (20, 1906.25),
    (21, 1753.90),
    (22, 1980.40),
]

BTC: list = [
    (9, 0.0008),
    (10, 0.07),
    (11, 0.95),
    (12, 13.44),
    (13, 817.36),
    (14, 314.24),
    (15, 430.05),
    (16, 963.74),
    (17, 13880.74),
    (18, 3843.52),
    (19, 7191.68),
    (20, 29001.19),
    (21, 39800.00),
]

# now for the main class for the charts


class TimeChart(ft.UserControl):
    def __init__(self):
        # some instances
        self.data_points: list = []
        self.points: list = GOLD    # start off with the gold prices frist
        # chart instance
        self.chart: ft.Control = ft.LineChart(
            # tooltip is the display price upon hovering
            tooltip_bgcolor=ft.colors.with_opacity(0.75, ft.colors.WHITE),
            expand=True,
            # we'll be using the min and max built-in function to get the min/
            # max of x and y
            # wrap it all in an int, so we avoid fractions
            min_y=int(min(self.points, key=lambda y: y[1])[1]),
            max_y=int(max(self.points, key=lambda y: y[1])[1]),
            min_x=int(min(self.points, key=lambda x: x[0])[0]),
            max_x=int(max(self.points, key=lambda x: x[0])[0]),
            # finally the axis labels
            left_axis=ft.ChartAxis(
                labels_size=50
            ),
            bottom_axis=ft.ChartAxis(
                labels_size=40,
                labels_interval=1
            )
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

        super().__init__()
    # we need two buttons to toggle between the two data sets
    def get_data_buttons(self, icon_name, btn_name, data):
        return ft.ElevatedButton(
            btn_name,
            color='white',
            icon=icon_name,
            width=140,
            height=40,
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=6)},
            ),
            bgcolor='teal600',
            data=data,
            on_click=lambda e: self.toggle_data(e)
        )

    # now, we need a way to toggle between each set while resseting the chart
    # along the way

    def toggle_data(self, e):
        self.switch_list(e)

        # next re-insert the line chart into the self.chart instance
        self.chart.data_series = [self.line_chart]

        # and finally, call the method below to get the new data points
        self.get_data_points()

    def switch_list(self, e):
        # print(e.control.data)
        if e.control.data == 'gold':
            self.points = GOLD
        if e.control.data == 'btc':
            self.points = BTC

        # after setting the data points list, we need reset the chart
        self.data_points = []
        self.chart.data_series = []
        self.line_chart.data_points = self.data_points

        # we need to reset the axis values as well
        self.chart.min_y = int(min(self.points, key=lambda y: y[1])[1])
        self.chart.max_y = int(max(self.points, key=lambda y: y[1])[1])
        self.chart.min_x = int(min(self.points, key=lambda x: x[0])[0])
        self.chart.max_x = int(max(self.points, key=lambda x: x[0])[0])

        self.chart.update()
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

    def build(self):
        self.line_chart.data_points = self.data_points
        self.chart.data_series = [self.line_chart]

        return ft.Column(
            horizontal_alignment='center',
            controls=[
                ft.Text(
                    "Yearly Historical Price for Bitcoin & Gold",
                    size=16,
                    weight='bold'
                ),
                self.chart,
            ],
        )
