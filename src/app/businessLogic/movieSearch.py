import requests
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

def getName(movie_id,media_type):
    if media_type =='tv':
        move_show = tmdb.tv(movie_id).details()
        return move_show.name
    elif media_type == 'movie':
        move_show = tmdb.movie(movie_id).details()
        return move_show.title
    else:
        return '[Failed To Load :(]'

def search_movies_and_tv_shows(query):
    url = 'https://api.themoviedb.org/3/search/multi'
    params = {
        'include_adult': 'false',
        'language': 'en-US',
        'page': 1,
        'query': query,  
        'api_key': '17766171d7b3067ced648bfe2ddc2a09',  # Replace with your TMDb API key
    }

    headers = {
        'Accept': 'application/json',
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            formatted_results = []

            for result in data['results']:
                if result['media_type'] in ['movie', 'tv']:
                    formatted_result = {
                        'id' : result['id'],
                        'title': result['title'] if result['media_type'] == 'movie' else result['name'],
                        'media_type': result['media_type'],
                        'overview': result['overview'],
                        'release_date': result['release_date'] if result['media_type'] == 'movie' else None,
                        'poster_path': result['poster_path']
                        # Add more fields as needed
                    }
                    formatted_results.append(formatted_result)

            return formatted_results
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Error while searching movies and TV shows: {str(e)}")
        return []