from flask import Flask, render_template, redirect, url_for

from wtforms_fields import *
from models import *

# Configure App
app = Flask(__name__)
app.secret_key = 'replace later'

#Configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://phzslmnqktoayb:c68a6d5b59a9709d7d254ca627bc999c8b5b23e11b7c47e8b25f2869ccb8fbaf@ec2-3-208-79-113.compute-1.amazonaws.com:5432/d8h8lveblshgp0'
db= SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():

    # update database if validation seccess
    reg_form= RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add user to database
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    
    login_form = LoginForm()

    #Allow login if validation success
    if login_form.validate_on_submit():
        return "Loged in, Finally!"

    return render_template("login.html",form = login_form)

if __name__ =="__main__":
    app.run(debug=True) 