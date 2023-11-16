import os

import mysql.connector
import pandas as pd
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri, conversion, default_converter


class ChartWithR:
    def __init__(self, name: str):
        self.name = name
        # Establecer la conexión a la base de datos
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Cralsive1620",
            database="dbproyecto"
        )
        self.cursor = self.conexion.cursor()

    def create_chart(self, specifications: dict):
        self.cursor.execute(specifications['query'])
        # Obtener los resultados de la consulta y convertirlos en un DataFrame de Pandas
        resultados = self.cursor.fetchall()
        result_dataset = pd.DataFrame(resultados, columns=[specifications["c_str"], specifications["c_num"]])
        df = result_dataset
        df[specifications["c_num"]] = df[specifications["c_num"]].apply(lambda x: round(x, 2))
        df[specifications["c_num"]] = df[specifications["c_num"]].astype(float)
        # Convertir el DataFrame de Pandas en un objeto R
        pandas2ri.activate()
        with conversion.localconverter(default_converter + rpy2.robjects.pandas2ri.converter):
            result_dataset_r = pandas2ri.py2rpy(df)

        robjects.globalenv['df'] = result_dataset_r

        # Cargar la biblioteca R base
        robjects.r('library(graphics)')
        path = str.replace(os.getcwd(), '\\', "/")

        # Crear una imagen de gráfico de barras en R
        robjects.r(f"""
                png(file="{path}/images/{self.name}.png", width=850, height=320)
                my_bar <- barplot(df${specifications["c_num"]}, names.arg = df${specifications["c_str"]}, 
                col = {specifications['color']}, main = "{specifications['tittle']}", 
                xlab ="{specifications['xlab']}", ylab="{specifications['ylab']}", ylim={specifications['ylim']})
                
                text(my_bar, df${specifications["c_num"]}-3 , paste("", df${specifications["c_num"]}, sep="") ,cex=1)
                dev.off()
                """)
