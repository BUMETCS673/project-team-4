import sys
sys.path.append("..")
from authentication.auth_utils import hash_password, verify_password
from database.db import connect_to_database, execute_query, insert_user_into_db,fetch_hashed_password,getValidationCode,alterValidationState,isAccountVerified
from verifymail import send_email,verification_code,VerifyCodeForm
from flask import Flask, render_template, request, flash, url_for, redirect
from businessLogic.movieSearch import get_popular

sender = "huangzhe406@gmail.com"
emailpassword = "mguvsoybbnterbkj"

def login(email,password,err):
    hashed_password_from_db = fetch_hashed_password(email)
    if hashed_password_from_db != None:
        flag=isAccountVerified(email)
        if flag[0]==0:
            login_errors={"loginemail":["Email address has not been veirfied!",]}
            login_errors.update(err)
            return render_template('index.html',errors=login_errors)
        if verify_password(password, hashed_password_from_db):
            return redirect(url_for('landing_page'))
        else:
            login_errors={"loginpassword":["Password error!"]}
            login_errors.update(err)
            return render_template('index.html',errors=login_errors)
    else:
        login_errors={"loginemail":["Email address has not been used to register, please registor first!"]}
        login_errors.update(err)
        return render_template('index.html',errors=login_errors)

def register(first_name,last_name,email,password,err):
    hashed_password = hash_password(password)
    vercode=verification_code()
    try:
        result = insert_user_into_db(first_name, last_name, email, hashed_password, vercode)
        if result:
            if send_email(subject='Verified Code',body=vercode, sender=sender, recipients=[email,], password=emailpassword):
                return redirect(url_for('verify'))
            else:
                flash("Registration failed, database is busy now")
                return render_template('index.html',errors=err)
        else:
            login_errors={"email":["This email address is used, try another email address!"]}
            return render_template('index.html',errors=login_errors)
    except Exception as e:
        print(f"Error during registration: {str(e)}")

def verification(userVerCode,userEmail,err):
    dbVerCode=getValidationCode(userEmail)[0]
    if userVerCode==dbVerCode:
        alterValidationState(email=userEmail)
        return redirect(url_for('landing_page'))
    else:
        flash("Verified code is incorrect!")
        return redirect(url_for('verify'))