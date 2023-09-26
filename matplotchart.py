import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import numpy as np
import matplotlib.pyplot as plt
import time
# now for the main class for the charts


class TimeMatPlotChart(ft.UserControl):
    def __init__(self, data_coin: list, data_weather: dict):
        self.gtq = []
        self.usd = []
        self.eur = []
        self.fechas = []
        for i in data_coin[0]:
            self.usd.append(round(float(i[1]), 3))
        for i in data_coin[1]:
            self.eur.append(round(float(i[1]), 3))
        for i in data_coin[2]:
            self.gtq.append(round(float(i[1]), 3))
        for i in data_coin[0]:
            self.fechas.append(i[0])

        self.promedio = []
        for x in data_weather:
            temp = []
            states = x["state_weather"]
            for c in states:
                data = c.values()
                for i in data:
                    if type(i) is dict:
                        temp.append(float(i["Promedio"]))
            self.promedio.append(round(np.mean(temp), 2))
        fig, ax1 = plt.subplots()
        ax1.plot(self.fechas, self.promedio)
        ax1.xaxis.set_ticks([0, 60, 120, 180, 240, 300, 360])
        ax2 = ax1.twinx()
        ax2.plot(self.fechas, self.usd, color="green")

        self.chart = MatplotlibChart(fig, isolated=True, expand=True)
        super().__init__()

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

    def toggle_data(self, e):
        self.switch_list(e)

    def switch_list(self, e):
        fig, ax1 = plt.subplots()
        if e.control.data == 'd1':
            ax1.plot(self.fechas, self.promedio)
            ax1.xaxis.set_ticks([0, 60, 120, 180, 240, 300, 360])
            ax2 = ax1.twinx()
            ax2.plot(self.fechas, self.usd, color="green")
        if e.control.data == 'd2':
            ax1.plot(self.fechas, self.promedio)
            ax1.xaxis.set_ticks([0, 60, 120, 180, 240, 300, 360])
            ax2 = ax1.twinx()
            ax2.plot(self.fechas, self.eur, color="purple")
        if e.control.data == 'd3':
            ax1.plot(self.fechas, self.promedio)
            ax1.xaxis.set_ticks([0, 60, 120, 180, 240, 300, 360])
            ax2 = ax1.twinx()
            ax2.plot(self.fechas, self.gtq, "red")

        self.chart.figure = fig
        self.chart.update()

    def build(self):
        return ft.Column(
            horizontal_alignment='center',
            controls=[
                self.chart,
            ],
        )
