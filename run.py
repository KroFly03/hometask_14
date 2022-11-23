from flask import Flask, jsonify
from utils import get_film_by_name, get_films_by_time_period, get_films_by_rating, get_last_films_by_genre


app = Flask(__name__)


@app.route('/')
def index():
    return ""


@app.route('/movie/<title>')
def film_by_title_view(title):
    film = get_film_by_name(title)
    return jsonify(film)


@app.route('/movie/<int:from_year>/to/<int:to_year>')
def films_by_time_period_view(from_year, to_year):
    films = get_films_by_time_period(from_year, to_year)
    return jsonify(films)


@app.route('/rating/<rating_category>')
def films_by_rating_view(rating_category):
    films = get_films_by_rating(rating_category)
    return jsonify(films)


@app.route('/genre/<genre>')
def films_by_genre_view(genre):
    films = get_last_films_by_genre(genre)
    return jsonify(films)


if __name__ == '__main__':
    app.run(debug=True)
