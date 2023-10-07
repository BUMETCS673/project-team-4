from flask import Flask, render_template, request, flash, url_for, redirect
from authentication.auth_utils import hash_password, verify_password
from database.db import connect_to_database, execute_query, insert_user_into_db,fetch_hashed_password,getValidationCode,alterValidationState
from businessLogic.movieSearch import get_popular
from validation import RegistrationForm
from verifymail import send_email,verification_code,VerifyCodeForm
from authentication.appControl import login,register,verification


app = Flask(__name__)
app.secret_key="random string"
sender = "huangzhe406@gmail.com"
emailpassword = "mguvsoybbnterbkj"

@app.route('/')
def main():
    form = RegistrationForm(request.form)
    err={"email":[],"password":[],"confirm_password":[]}
    return render_template('index.html',form=form,errors=err)

@app.route('/home', methods=['GET','POST'])
def accessPage():
    form = RegistrationForm(request.form)
    err={"email":[],"password":[],"confirm_password":[]}
    if request.form['submit'] == 'Login':
        email = request.form['email']
        password = request.form['password']
        return login(email=email,password=password,err=form.errors)

    elif request.form['submit'] == 'Register':
        firstName= request.form['firstName']
        lastName= request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        if form.validate():
            return register(firstName=firstName,lastName=lastName,email=email,password=password,err=form.errors)
        else:
            return render_template('index.html',errors=form.errors)

    return render_template('index.html',form=form,errors=err)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    form=VerifyCodeForm(request.form)
    err={}
    if request.method == 'POST':
        userVerCode=request.form['verifycode']
        userEmail=request.form['email']
        return verification(userVerCode=userVerCode,userEmail=userEmail,err=form.errors)
    return render_template('verify.html',errors=form.errors)


    
@app.route('/landing-page', methods=['GET', 'POST'])
def landingPage():
    popular_movies, popular_tv_shows = get_popular()
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


if __name__ == '__main__':
    app.jinja_env.cache = {}
    app.run()
