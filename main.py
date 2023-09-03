import datetime
from dynamodb import DynamoDB

db = DynamoDB()
exitw = False

while not exitw:
    print('-------------------------------------------')
    print('1. Ver toda la tabla')
    print('2. Buscar un dato en especifico')
    print('3. Insertar un dato')
    print('4. SALIR')
    option = input('Ingrese una opcion: ')

    match option:
        case '1':
            print('Table Country')
            db.show_table()
        case '2':
            country_id = 'NONE'
            print('Table Country Query')
            search = input('Ingrese el pais a buscar: ')
            db.query_dataC(search)
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
                    db.query_dataCC(query_2)
                    print('WEATHER')
                    query_1 = str(date) + country_id + '-W'
                    db.query_dataCW(query_1)
                    date += datetime.timedelta(days=1)

        case '3':
            print('Table Country Insert')
            country = {'name': input('Ingrese el nombre del pais: '),
                       'contry_id': input('Ingrese pais: ')}
            db.insert_dataC(country)
            country_coin = {'id': input('Ingrese dato: '),
                            'contry_id': input("Ingrese pais: ")}
            db.insert_dataCC(country_coin)
            contry_weather = {'id': input('Ingrese dato: '),
                              'contry_id': input('Ingrese pais: ')}
            db.insert_dataCW(contry_weather)

        case '4':
            exitw = True

    print('-----------------------------------------------------------')

