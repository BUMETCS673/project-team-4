from flask import Flask, render_template, request
from themoviedb import TMDb
from justwatch import JustWatch
from canistreamit import search, streaming, rental, purchase, dvd, xfinity
from authentication.auth_utils import hash_password, verify_password
from database.db import connect_to_database, execute_query, insert_user_into_db,fetch_hashed_password_and_salt



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
        hashed_password_from_db, salt_from_db = fetch_hashed_password_and_salt(email)

        if hashed_password_from_db and verify_password(password, hashed_password_from_db, salt_from_db):
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
            print("Passowrd didn't match")

    display_movies_and_tv_shows()
    '''return render_template('landing_page.html',
                           popular_movies = popular_movies['items'],
                           popular_tv_shows = popular_tv_shows['items'])'''


def display_movies_and_tv_shows():
    print("Loading and get Movie Data")
    popular_tv_shows = showFinder.search_for_item(content_types = ['show'])['items']
    '''
    for show in popular_tv_shows:
        print(search(show['title']))
        print(streaming(search(show['title'])[0]['_id']))
    '''
    popular_movies = showFinder.search_for_item(content_types = ['movie'])['items']
    print(popular_tv_shows[0]['title'])
    return render_template('landing_page.html',
                           popular_movies = popular_movies,
                           popular_tv_shows = popular_tv_shows)
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