from flask import Flask, render_template, request
from businessLogic.movieSearch import get_popular, search_movies_and_tv_shows
from validation import RegistrationForm
from verifymail import VerifyCodeForm
from authentication.appControl import login, register, verification

app = Flask(__name__)
app.secret_key = "random string"
sender = "huangzhe406@gmail.com"
emailpassword = "mguvsoybbnterbkj"


'''
Main function for app
'''
@app.route('/')
def main():
    form = RegistrationForm(request.form)
    err = {"email": [], "password": [], "confirm_password": []}
    return render_template('index.html', form=form, errors=err)


'''
First page that is opened on the BUMTV site
You may register or login to an existing account
'''
@app.route('/home', methods=['GET', 'POST'])
def access_page():
    form = RegistrationForm(request.form)
    err = {"email": [], "password": [], "confirm_password": []}
    if request.form['submit'] == 'Login':
        email = request.form['email']
        password = request.form['password']
        return login(email=email, password=password, err=form.errors)
    elif request.form['submit'] == 'Register':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        if form.validate():
            return register(first_name=first_name, last_name=last_name, email=email, password=password, err=form.errors)
        else:
            return render_template('index.html', errors=form.errors)
    return render_template('index.html', form=form, errors=err)


'''
Verifies the code entered is the one that was sent prior to creating the account
'''
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    form = VerifyCodeForm(request.form)
    if request.method == 'POST':
        userVerCode = request.form['verifycode']
        userEmail = request.form['email']
        return verification(userVerCode=userVerCode, userEmail=userEmail, err=form.errors)
    return render_template('verify.html', errors=form.errors)


'''
Landing page once a user is logged into the app
'''
@app.route('/landing-page', methods=['GET', 'POST'])
def landing_page():
    popular_movies, popular_tv_shows = get_popular()
    return render_template('landing_page.html',
                           popular_movies=popular_movies,
                           popular_tv_shows=popular_tv_shows)


'''
Display search results for a user
'''
@app.route('/search')
def search_results():
    query = request.args.get('query')
    results = search_movies_and_tv_shows(query)
    return render_template('search_results.html', query=query, results=results)


'''
Profile page for a user
'''
@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
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


if __name__ == '__main__':
    app.jinja_env.cache = {}
    app.run()
