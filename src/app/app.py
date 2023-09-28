from flask import Flask, render_template, request,flash
from themoviedb import TMDb
from justwatch import JustWatch
from canistreamit import search, streaming, rental, purchase, dvd, xfinity
from authentication.auth_utils import hash_password, verify_password
from database.db import connect_to_database, execute_query, insert_user_into_db,fetch_hashed_password
from validation import RegistrationForm



app = Flask(__name__)
app.secret_key="random string"

#tmdb = TMDb(api_key='API Key when we recieve one')

showFinder= JustWatch(country='US')

@app.route('/')
def main():
    form = RegistrationForm(request.form)
    err={"email":[],"password":[],"confirm_password":[]}
    return render_template('index.html',form=form,errors=err)

@app.route('/home', methods=['GET','POST'])
def accessPage():
    # print(request.form['submit'])
    form = RegistrationForm(request.form)
    err={"email":[],"password":[],"confirm_password":[]}
    if request.form['submit'] == 'Login':
        email = request.form['email']
        password = request.form['password']
        hashed_password_from_db = fetch_hashed_password(email)

        if hashed_password_from_db and verify_password(password, hashed_password_from_db):
            flash("Login successful")
        else:
            flash("Login failed")


    elif request.form['submit'] == 'Register':
        firstName= request.form['firstName']
        lastName= request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if form.validate():
            hashed_password = hash_password(password)

            try:
                result = insert_user_into_db(firstName, lastName, email, hashed_password)
                if result:
                    flash("Registration successful")
                else:
                    flash("Registration failed, database is busy now")
            except Exception as e:
                print(f"Error during registration: {str(e)}")
        else:
            return render_template('index.html',form=form,errors=err)

    display_movies_and_tv_shows()
    '''return render_template('landing_page.html',
                           popular_movies = popular_movies['items'],
                           popular_tv_shows = popular_tv_shows['items'])'''
    return render_template('index.html',form=form,errors=err)


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
    app.run()
