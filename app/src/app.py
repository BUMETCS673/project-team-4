from flask import Flask, render_template, request
from themoviedb import TMDb
from justwatch import JustWatch
from canistreamit import search, streaming, rental, purchase, dvd, xfinity

app = Flask(__name__)


#tmdb = TMDb(api_key='API Key when we recieve one')

showFinder= JustWatch(country='US')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/home', methods=['GET','POST'])
def accessPage():
    print(request.form['submit'])
    if request.form['submit'] == 'Login':
        email = request.form['email']
        password = request.form['password']
    elif request.form['submit'] == 'Register':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
    print("Loading Movie Data")
    popular_tv_shows = showFinder.search_for_item(content_types = ['show'])['items']
    '''
    for show in popular_tv_shows:
        print(search(show['title']))
        print(streaming(search(show['title'])[0]['_id']))
    '''
    popular_movies = showFinder.search_for_item(content_types = ['movie'])['items']
    print(popular_tv_shows['items'][0]['title'])
    return render_template('landing_page.html',
                           popular_movies = popular_movies['items'],
                           popular_tv_shows = popular_tv_shows['items'])
    #display_movies_and_tv_shows()
    #return render_template("landing_page.html")


def display_movies_and_tv_shows():
    print("Load and get Movie Data")
    popular_tv_shows = showFinder.popular_tv_shows(limit=10)
    popular_movies = showFinder.popular_movies(limit=10)
    return render_template('landing_page.html',
                           popular_movies=popular_movies,
                           popular_tv_shows=popular_tv_shows)
    '''
    # Fetch a list of popular movies and TV shows (customize as needed)
    popular_movies = tmdb.movie.popular()
    popular_tv_shows = tmdb.tv.popular()

    # Pass the data to your HTML template
    return render_template('landing_page.html',
                           popular_movies=popular_movies,
                           popular_tv_shows=popular_tv_shows)
'''
if __name__ == '__main__':
    app.run(debug=True)