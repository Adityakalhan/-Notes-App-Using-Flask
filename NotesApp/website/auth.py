from flask import Blueprint,render_template,request,flash
from flask import redirect,url_for
from . import db 
from .models import User,Note
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user
auth = Blueprint('auth',__name__) #setting up a blueprint for the flask application


@auth.route('/login',methods = ['GET','POST'])
def login() :
    if request.method == 'POST' :
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email = email).first() #checking if there is a user with this email
        if user :
            if check_password_hash(user.password,password) : 
                flash("Login successful!",category='success')
                login_user(user,remember=True)

                return redirect(url_for('views.home'))
            else :
                flash("Please check the email or password",category = 'error')
        else :
            flash('User not found',category='error')


    return render_template('login.html',user = current_user)

@auth.route('/logout')
@login_required
def logout() :
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods = ['GET','POST'])
def signup() :
    if request.method == 'POST' :
        email = request.form.get('email')
        firstname = request.form.get('FirstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email = email).first()
        if user :
            flash('Email already in use',category='error')
        elif len(email) < 4 :
            flash("Email must be greater than 3 characters",category='error')
        elif len(firstname) < 2 :
            flash("Name must be greater than 1 character",category='error')
        elif password1 != password2 :
            flash("Passwords don't match",category='error')
        elif len(password1) < 7 :
            flash("Length of password must be greater than 7",category='error')
        else :
            new_user = User(email = email,FirstName = firstname, password = generate_password_hash(password1,method = 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("Account Created !",category='success')
            return redirect(url_for('views.home'))

            #add to db

    return render_template('sign_up.html',user = current_user)