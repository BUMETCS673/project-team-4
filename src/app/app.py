from flask import Flask, render_template, request, flash, url_for, redirect
from authentication.auth_utils import hash_password, verify_password
from database.db import connect_to_database, execute_query, insert_user_into_db,fetch_hashed_password,getValidationCode,alterValidationState
from businessLogic.movieSearch import get_popular
from validation import RegistrationForm
from verifymail import send_email,verification_code,VerifyCodeForm


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
    # print(request.form['submit'])
    form = RegistrationForm(request.form)
    err={"email":[],"password":[],"confirm_password":[]}
    if request.form['submit'] == 'Login':
        email = request.form['email']
        password = request.form['password']
        hashed_password_from_db = fetch_hashed_password(email)

        if hashed_password_from_db and verify_password(password, hashed_password_from_db):
            flash("Login successful")
            return display_movies_and_tv_shows()
        else:
            flash("Login failed")


    elif request.form['submit'] == 'Register':
        if not form.validate():
            print(form.errors)
            return render_template('index.html',errors=form.errors)
        firstName= request.form['firstName']
        lastName= request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if form.validate():
            hashed_password = hash_password(password)
            vercode=verification_code()
            try:
                result = insert_user_into_db(firstName, lastName, email, hashed_password,vercode)
                if result:
                    if not send_email(subject='Verified Code',body=vercode, sender=sender, recipients=[email,], password=emailpassword):
                        print('err')
                    return redirect(url_for('verify'))
                else:
                    flash("Registration failed, database is busy now")
            except Exception as e:
                print(f"Error during registration: {str(e)}")
        else:
            return render_template('index.html',errors=err)

    # display_movies_and_tv_shows()
    '''return render_template('landing_page.html',
                           popular_movies = popular_movies['items'],
                           popular_tv_shows = popular_tv_shows['items'])'''
    return render_template('index.html',form=form,errors=err)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    form=VerifyCodeForm(request.form)
    err={}
    if request.method == 'POST':
    # if request.form['submit'] == 'Verify':
        # return render_template('verify.html',errors=err)
        userVerCode=request.form['verifycode']
        userEmail=request.form['email']
        dbVerCode=getValidationCode(userEmail)[0]
        if userVerCode==dbVerCode:
            alterValidationState(email=userEmail)
            # return render_template('index.html',errors=err)
            return display_movies_and_tv_shows()
        else:
            flash("Verified code is incorrect!")
            return redirect(url_for('verify'))
    return render_template('verify.html',errors=err)


def display_movies_and_tv_shows():
    popular_movies, popular_tv_shows = get_popular()
    return landingPage()
    
    
@app.route('/landing-page', methods=['GET', 'POST'])
def landingPage():
    popular_movies, popular_tv_shows = get_popular()
    return landingPage()
    
    
@app.route('/landing-page', methods=['GET', 'POST'])
def landingPage():
    popular_movies, popular_tv_shows = get_popular()
    return landingPage()
    
    
@app.route('/landing-page', methods=['GET', 'POST'])
def landingPage():
    popular_movies, popular_tv_shows = get_popular()
    return landingPage()
    
    
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
