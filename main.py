import datetime
import mysqlConection

db = mysqlConection
exitw = False

while not exitw:
    print('-------------------------------------------')
    print('1. Cargar Datos')
    print('2. Buscar un dato en especifico')
    print('3. Insertar un dato')
    print('4. SALIR')
    option = input('Ingrese una opcion: ')

    match option:
        case '1':
            # Obtener datos de DynamoDB
            datos_mongodb_country, datos_mongodb_states = db.extraer_datos_de_mongoCountry()
            datos_mongodb_coin = db.extraer_datos_de_mongodbCoin()
            datos_mongodb_cweather, datos_mongodb_weather = db.extraer_datos_de_mongodbWeather()

            print(datos_mongodb_coin)
            # Insertar los datos en MySQL
            #db.insertar_datos_en_mysqlCountry(db.conexion_mysql, datos_mongodb_country)
            #db.insertar_datos_en_mysqlStates(db.conexion_mysql, datos_mongodb_states)
            #db.insertar_datos_en_mysqlCoin(db.conexion_mysql, datos_mongodb_coin)

            #db.insertar_datos_en_mysqlCWeather(db.conexion_mysql, datos_mongodb_cweather)
            #db.insertar_datos_en_mysqlWeather(db.conexion_mysql, datos_mongodb_weather)
        case '2':

            print('Table Country Query')
            # Solicitar al usuario que ingrese el país a buscar
            busqueda = input("Ingrese el nombre del pais a buscar")
            db.query_MysqlCountry(busqueda)
            print('Ingrese la fecha de inico para obtener los datos YYYY-mm-dd:')
            year = int(input('Ingrese el año: '))
            month = int(input('Ingrese el mes: '))
            day = int(input('Ingrese el dia: '))
            date = datetime.date(year, month, day)
            while date < datetime.date.today():
                print('DATOS CON RESPECTO A LA FECHA: ' + str(date))
                print('COIN')
                query_2 = str(date) + 'GT' + '-C'
                db.query_dataCC(query_2)

        case '3':
            pass

        case '4':
            exitw = True


# Cerrar la conexión a MySQL
db.cursor_mysql.close()
db.conexion_mysql.close()
