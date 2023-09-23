from flask import Flask, render_template, request
from themoviedb import aioTMDb

app = Flask(__name__)


#tmdb = aioTMDb(api_key='API Key when we recieve one')

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
        firstName= request.form['First Name']
        lastName= request.form['Last Name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
    display_movies_and_tv_shows()
    return render_template("landing_page.html")


async def display_movies_and_tv_shows():
    print("Load and get Movie Data")
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