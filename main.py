from flask import Flask, redirect, url_for,render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.secret_key = "TEST"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.sqlite3'
db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column("ID", db.Integer, primary_key=True)
    _firstName = db.Column("FirstName", db.String(100))
    _lastname = db.Column("LastName", db.String(100))
    _username = db.Column("UserName", db.String(100))
    _Password = db.Column("Password", db.String(100))
    _Email = db.Column("Email", db.String(100))

    def __init__(self,firstname,lastname,username,password,email): #Constructor For A User Object
        self._firstName = firstname
        self._lastname = lastname
        self._username = username
        self._Email = email
        self._Password = password

@app.route("/")
def HomePage():
    return redirect(url_for("SignInPage"))
    

@app.route("/SignIn", methods=['GET','POST'])
def SignInPage():
    if request.method == "GET":
        return render_template("SignInHTMLPage.html")
    else:
        userNameLoginInput = request.form['username']
        passwordLoginInput = request.form['password']

        loggedInUser = Users.query.filter_by(_username=userNameLoginInput).first()
        if loggedInUser == None:
            return "Wrong User Name"
        if not loggedInUser or not check_password_hash(loggedInUser._Password, passwordLoginInput):
            return "Wrong Password"
        else:
            return redirect(url_for("UserHomePage"))

        #if Users.query.filter_by(_username=userNameLoginInput).first():
            #return render_template("UserHomePage.html")
        #else:
            #return "Wrong Username"


@app.route("/SignUp", methods=['GET','POST'])
def SignUp():
    if request.method == "GET": #when the page is loaded
        #user_test = users()
        #user_test._firstName = "Marwan"
        #db.session.add(user_test)
        #db.session.commit()
        return render_template("SignUpHTMLPage.html")
    else: #method.request == "POST"
        userNameDuplicationFlag = Users.query.filter_by(_username=request.form['username']).first()
        if userNameDuplicationFlag == None:
            UserObject = Users(firstname=request.form['fname'],lastname=request.form['lname'],username=request.form['username'],password=generate_password_hash(request.form['password'],'sha256'),email=request.form['UserEmail'])
            db.session.add(UserObject)
            db.session.commit()
            return "thank you"
        else:
            return "Username Duplication"

@app.route("/UserHomePage")
def UserHomePage():
    return render_template("UserHomePage.html")

if __name__ == '__main__':
    db.create_all()
    app.run()

