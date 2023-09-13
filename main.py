import datetime
from dynamodb import DynamoDB

db = DynamoDB()
exitw = False

while not exitw:
    print('-------------------------------------------')
    print('1. Cargar datos de un pais en especifico')
    print('2. Buscar un dato en especifico')
    print('3. Insertar un dato')
    print('4. SALIR')
    option = input('Ingrese una opcion: ')

    match option:
        case '1':
            pais = input('Ingrese el pais a trasladar: ')
            # Obtener datos de MongoDB
            datos_mongodb_country = db.get_country_data_from_mongodb(pais)
            datos_mongodb_coin = db.get_country_coin_data_from_mongodb()
            datos_mongodb_weather = db.get_country_weather_data_from_mongodb()
            # Insertar los datos en DyanamoDB
            for data in datos_mongodb_country:
                db.insert_data_country(data)
            for data in datos_mongodb_coin:
                db.insert_data_country_coin(data)
            for data in datos_mongodb_weather:
                db.insert_data_country_weather(data)

        case '2':
            print('Table Country Query')
            search = input('Ingrese el pais a buscar: ')
            db.query_data_country(search)
            country_id = db.get_country_id()
            if country_id != 'NONE':
                print('Ingrese la fecha de inico para obtener los datos YYYY-mm-dd:')
                year = int(input('Ingrese el año: '))
                month = int(input('Ingrese el mes: '))
                day = int(input('Ingrese el dia: '))
                date = datetime.date(year, month, day)
                while date < datetime.date.today():
                    print('DATOS CON RESPECTO A LA FECHA: ' + str(date))
                    print('COIN')
                    query_2 = str(date) + country_id + '-C'
                    db.query_data_country_coin(query_2)
                    print('WEATHER')
                    query_1 = str(date) + country_id + '-W'
                    db.query_data_country_weather(query_1)
                    date += datetime.timedelta(days=1)

        case '3':
            print('Table Country Insert')
            country = {'name': input('Ingrese el nombre del pais: '),
                       'contry_id': input('Ingrese pais: ')}
            db.insert_data_country(country)
            country_coin = {'id': input('Ingrese dato: '),
                            'contry_id': input("Ingrese pais: ")}
            db.insert_dataCC(country_coin)
            contry_weather = {'id': input('Ingrese dato: '),
                              'contry_id': input('Ingrese pais: ')}
            db.insert_dataCW(contry_weather)

        case '4':
            exitw = True

    print('-----------------------------------------------------------')
