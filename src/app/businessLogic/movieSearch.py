from themoviedb import TMDb
from justwatch import JustWatch
from canistreamit import search, streaming, rental, purchase, dvd, xfinity


tmdb = TMDb(key='17766171d7b3067ced648bfe2ddc2a09')

showFinder= JustWatch(country='US')

def get_popular():
    popular_tv_shows = tmdb.trending().tv_weekly().results
    #popular_tv_shows = showFinder.search_for_item(content_types = ['show'])['items']
    '''
    for show in popular_tv_shows:
        print(search(show['title']))
        print(streaming(search(show['title'])[0]['_id']))
    '''
    popular_movies = tmdb.trending().movie_weekly().results
    #popular_movies = showFinder.search_for_item(content_types = ['movie'])['items']
    popular_movies= popular_movies
    popular_tv_shows = popular_tv_shows
    return popular_movies, popular_tv_shows 