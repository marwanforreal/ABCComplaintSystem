from flask import Flask, redirect, url_for,render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.secret_key = "TEST"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ABC.sqlite3'
db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column("ID", db.Integer, primary_key=True)
    _firstName = db.Column("FirstName", db.String(100))
    _lastname = db.Column("LastName", db.String(100))
    _username = db.Column("UserName", db.String(100))
    _Password = db.Column("Password", db.String(100))
    _Email = db.Column("Email", db.String(100))
    _complaints = db.relationship('Complaints', backref='ComplaintWriter',lazy='dynamic')


class Complaints(db.Model):
    _id = db.Column("ComplaintID", db.Integer, primary_key=True)
    _UserID = db.Column("UserID", db.Integer,db.ForeignKey('users.ID'))
    _title = db.Column("Title", db.String(30))
    _Category = db.Column("Category", db.String(20))
    _ComplaintMessage = db.Column("ComplaintMessage", db.String(300))
    _complaintStatus = db.Column("ComplaintStatus", db.String(30))



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
            session['LoggedInUser'] = loggedInUser._username
            return redirect(url_for("UserHomePage", user=loggedInUser._username))




@app.route("/SignUp", methods=['GET','POST'])
def SignUp():
    if request.method == "GET": #when the page is loaded
        return render_template("SignUpHTMLPage.html")
    else: #method.request == "POST"
        userNameDuplicationFlag = Users.query.filter_by(_username=request.form['username']).first()
        if userNameDuplicationFlag == None:
            UserObject = Users(_firstName=request.form['fname'],_lastname=request.form['lname'],_username=request.form['username'],_Password=generate_password_hash(request.form['password'],'sha256'),_Email=request.form['UserEmail'])
            db.session.add(UserObject)
            db.session.commit()
            return "thank you"
        else:
            return "Username Duplication"

@app.route("/UserHomePage/<user>", methods=['GET','POST'])
def UserHomePage(user): #THIS IS WHERE YOU SEND COMPLAINTS
    if request.method == 'GET':
        return render_template("UserHomePage.html")
    else:
        complainingUserObject = Users.query.filter_by(_username=user).first()
        ComplaintObject = Complaints(_title=request.form['title'],_Category=request.form['category'],_ComplaintMessage=request.form['complaint'],ComplaintWriter=complainingUserObject, _complaintStatus='Pending Resolution')

        db.session.add(ComplaintObject)
        db.session.commit()
        return "thank you"

@app.route("/TicketStatus")
def TicketStatus():

    if 'LoggedInUser' in session:
        ListOfComplaintTitles=[]
        ListOfComplaintStatus=[]
        complainingUserObject = Users.query.filter_by(_username=session['LoggedInUser']).first()
        CurrentUserID = complainingUserObject._id
        ComplaintObjects = Complaints.query.filter_by(_UserID=CurrentUserID).all() #returns a list of objects

        for x in range(len(ComplaintObjects)): #To transform the list of objects to a list of strings that can be used in html
            ListOfComplaintTitles.append(ComplaintObjects[x]._title)
            ListOfComplaintStatus.append(ComplaintObjects[x]._complaintStatus)


        return render_template("TicketStatus.html", ListOfComplaints=ListOfComplaintTitles, status=ListOfComplaintStatus, len=len(ComplaintObjects))

if __name__ == '__main__':
    db.create_all()
    app.run()
