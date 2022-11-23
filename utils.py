import sqlite3
import pprint
DATABASE = 'netflix.db'


def sql_single_data_reader(query):
    """Вывод данных с пользовательских запросов одной записи"""
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchone()

        return data


def sql_many_data_reader(query):
    """Вывод данных с пользовательских запросов множества записей"""
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        return data


def get_film_by_name(name):
    """Вывод информации о фильме по его названию"""
    query = f"""
                select title, country, release_year, listed_in, description from netflix
                where title = '{name}'
            """
    data = sql_single_data_reader(query)

    json = []

    film = {
        'title': data[0],
        'country': data[1],
        'release_year': data[2],
        'listed_in': data[3],
        'description': data[4],
    }

    json.append(film)

    return json


def get_films_by_time_period(from_year, to_year):
    """Вывод информации о фильмах по временному промежутку"""
    query = f"""
                    select title, release_year from netflix
                    where release_year between {from_year} and {to_year}
                    limit 100
                """
    data = sql_many_data_reader(query)

    json = []

    for i in data:
        film = {
            'title': i[0],
            'release_year': i[1],
        }
        json.append(film)

    return json


def define_rating_names(rating_category):
    """Получение названий рейтингов исходя из категории"""
    match(rating_category.lower()):
        case 'children':
            return ["'G'"]
        case 'family':
            return ["'G'", "'PG'", "'PG-13'"]
        case 'adult':
            return ["'R'", "'NC-17'"]
        case null:
            return null


def get_films_by_rating(rating_category):
    """Вывод информации о фильмах по выбранной категории рейтинга"""
    rating_names = define_rating_names(rating_category)

    query = f"""
                        select title, rating, description from netflix
                        where rating in ({', '.join(rating_names)})
                        limit 100
                    """
    data = sql_many_data_reader(query)

    json = []

    for i in data:
        film = {
            'title': i[0],
            'rating': i[1],
            'description': i[2],
        }
        json.append(film)

    return json


def get_last_films_by_genre(genre):
    """Вывод информации о 10 новейшних фильмах по выбранному жанру"""

    query = f"""
                        select title, description from netflix
                        where '{genre}' in (listed_in)
                        order by release_year
                        limit 10
                    """
    data = sql_many_data_reader(query)

    json = []

    for i in data:
        film = {
            'title': i[0],
            'description': i[1],
        }
        json.append(film)

    return json


def get_actors_list_played_with(actor1, actor2):
    """Вывод информации о актерах, которые снимались в фильмах больше двух раз с выбранными двумя"""

    query = f"""
                        select [cast], count([cast]) from netflix
                        where [cast] like '%{actor1}%' and [cast] like '%{actor2}%' 
                        group by [cast]
                    """
    data = sql_many_data_reader(query)

    return data


def get_films_by_filters(type, release_year, genre):
    """Вывод информации о фильмах по выбранным типу, году выпуска и жанру"""

    query = f"""
                            select * from netflix
                            where type = '{type}'
                            and release_year = {release_year}
                            and listed_in like '%{genre}%'
                        """
    data = sql_many_data_reader(query)

    return data
