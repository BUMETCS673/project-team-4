from flask import Flask, render_template, request
from themoviedb import TMDb
from justwatch import JustWatch
from canistreamit import search, streaming, rental, purchase, dvd, xfinity
from authentication.auth_utils import hash_password, verify_password
from database.db import connect_to_database, execute_query, insert_user_into_db,fetch_hashed_password



app = Flask(__name__)


tmdb = TMDb(key='17766171d7b3067ced648bfe2ddc2a09')

showFinder= JustWatch(country='US')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/home', methods=['GET','POST'])
def landingPage():
    print(request.form['submit'])
    if request.form['submit'] == 'Login':
        email = request.form['email']
        password = request.form['password']
        hashed_password_from_db = fetch_hashed_password(email)

        if hashed_password_from_db and verify_password(password, hashed_password_from_db):
            print("Login successful")
        else:
            print("Login failed")


    elif request.form['submit'] == 'Register':
        firstName= request.form['firstName']
        lastName= request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if confirm_password == password:
            hashed_password = hash_password(password)

            try:
                result = insert_user_into_db(firstName, lastName, email, hashed_password)
                if result:
                    print("Registration successful")
                else:
                    print("Registration failed")
            except Exception as e:
                print(f"Error during registration: {str(e)}")
        else:
            print("Password didn't match")
    
    popular_movies, popular_tv_shows = display_movies_and_tv_shows()
    return render_template('landing_page.html',
                           popular_movies = popular_movies,
                           popular_tv_shows = popular_tv_shows)
    
@app.route('/profile', methods=['GET','POST'])
def profilePage():
    # TEST VALUES
    user_name = "John Doe"  # Replace with the user's actual name
    user_email = "john.doe@example.com"  # Replace with the user's actual email
    watch_list = [
        {"title": "Movie 1"},
        {"title": "Movie 2"},
    ]

    return render_template('profile_page.html', user_name=user_name, 
                           user_email=user_email, 
                           watch_list=watch_list)

def display_movies_and_tv_shows():
    print("Loading and get Movie Data")
    popular_tv_shows = tmdb.trending().tv_weekly().results
    #popular_tv_shows = showFinder.search_for_item(content_types = ['show'])['items']
    '''
    for show in popular_tv_shows:
        print(search(show['title']))
        print(streaming(search(show['title'])[0]['_id']))
    '''
    popular_movies = tmdb.trending().movie_weekly().results
    #popular_movies = showFinder.search_for_item(content_types = ['movie'])['items']
    print(popular_movies[0].overview)
    popular_movies= popular_movies
    popular_tv_shows = popular_tv_shows
    return popular_movies, popular_tv_shows 


if __name__ == '__main__':
    app.jinja_env.cache = {}
    app.run()
