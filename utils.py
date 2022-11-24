import sqlite3
import pprint
DATABASE = 'netflix.db'


def sql_data_reader(query):
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
                order by release_year desc 
                limit 1
            """
    data = sql_data_reader(query)
    print(data)
    json = []

    film = {
        'title': data[0][0],
        'country': data[0][1],
        'release_year': data[0][2],
        'listed_in': data[0][3],
        'description': data[0][4],
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
    data = sql_data_reader(query)

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
    data = sql_data_reader(query)

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
    data = sql_data_reader(query)

    json = []

    for i in data:
        film = {
            'title': i[0],
            'description': i[1],
        }
        json.append(film)

    return json


def get_actor_plays_count(data, actor1, actor2):
    """Получает сведение о том, сколько разные актеры снимались с определенными"""

    actor_plays_count = {
        'actors': [],
        'counts': []
    }

    for actors in data:
        actors = ' '.join(actors).split()
        for actor in actors:
            if actor not in [actor1, actor2]:
                if actor not in actor_plays_count['actors']:
                    actor_plays_count['actors'].append(actor)
                    actor_plays_count['counts'].append(0)
                else:
                    index = actor_plays_count['actors'].index(actor)
                    actor_plays_count['counts'][index] += 1

    return actor_plays_count


def get_actors_list_played_with(actor1, actor2):
    """Вывод информации о актерах, которые снимались в фильмах больше двух раз с выбранными двумя"""

    query = f"""
                        select [cast] from netflix
                        where [cast] like '%{actor1}%' and [cast] like '%{actor2}%' 
                    """
    data = sql_data_reader(query)

    all_actors = get_actor_plays_count(data, actor1, actor2)

    actors = [actor for i, actor in enumerate(all_actors['actors']) if all_actors['counts'][i] > 1]

    return actors


def get_films_by_filters(type, release_year, genre):
    """Вывод информации о фильмах по выбранным типу, году выпуска и жанру"""

    query = f"""
                            select * from netflix
                            where type = '{type}'
                            and release_year = {release_year}
                            and listed_in like '%{genre}%'
                        """
    data = sql_data_reader(query)

    return data
