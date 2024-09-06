import psycopg2
from config import host,password,user,db_name
from datetime import datetime,timedelta



def create_table():
    try:
        connection=psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit=True
        with connection.cursor() as cursor:
            cursor.execute(
                 """
                CREATE TABLE urls(
                id serial PRIMARY KEY,
                url varchar(150) NOT NULL,
                date date);
                create unique index duplicate on urls(url);
                CREATE TABLE info_flats(
                id serial PRIMARY KEY,
                url varchar(150) NOT NULL REFERENCES urls(url) ON DELETE CASCADE,
                status text,
                price integer,
                date date,
                descr text,
                year text
                );
                create unique index duplicate on info_flats(url);
                """
            )
        print('Таблица создана')
    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()
        


# CREATE TABLE info_flats(
#                 id serial PRIMARY KEY,
#                 url varchar(150) NOT NULL REFERENCES urls(url) ,
#                 status text,
#                 price integer,
#                 date date,
#                 descr text,
#                 year text,
#                 date_test date
#                 );
#                 create unique index duplicate on info_flats(url);


def get_urls(url,date):
    try:
        connection=psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit=True
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO urls(
                url,
                date
                ) VALUES 
                (%s,%s);""",
                (url,date,)
            )
        print('Данные успешно вставлены')
    except Exception as ex:
        print('Произошла ошибка',ex)

    finally:
        if connection:
            connection.close()
            
def vstavka_in_info_flats(url,status,price,date,descr,year):
    try:
        connection=psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit=True
        
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO info_flats(
                url, status, price, date, descr, year
                ) VALUES 
                (%s,%s,%s,%s,%s,%s);""",
                (url,status,price, date,descr,year,) 
            )
        print('Данные успешно вставлены')
    except Exception as ex:
        print('Произошла ошибка',ex)

    finally:
        if connection:
            connection.close()




def select_urls():
    try:
        connection=psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit=True
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                    SELECT * 
                    FROM urls
                    where CURRENT_DATE-date=0
                    order by date DESC
                """
            )
            print('Данные из таблицы получены')
            return cursor.fetchall()
    except Exception as ex:
        print('Произошла ошибка',ex)

    finally:
        if connection:
            connection.close()
            
            
def select_from_info_flats():
    try:
        connection=psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit=True
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                    SELECT url,status,price,descr,year 
                    FROM info_flats 
                    where CURRENT_DATE-date=0
                    order by year DESC, price asc
                """
            )
            print('Данные из таблицы получены')
            return cursor.fetchall()
    except Exception as ex:
        print('Произошла ошибка',ex)

    finally:
        if connection:
            connection.close()

# clear_table()
