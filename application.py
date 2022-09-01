from flask import Flask, render_template

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

    reg_form= RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        
        # Add user to database
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into database!"

    return render_template("index.html", form=reg_form)
if __name__ =="__main__":
    app.run(debug=True) 