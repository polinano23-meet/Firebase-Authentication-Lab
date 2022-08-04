from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyCQ7kDtpsnUPViaMcPieLlmuNvCzHFaB0g",
  "authDomain": "final-mini-project-6f22d.firebaseapp.com",
  "projectId": "final-mini-project-6f22d",
  "storageBucket": "final-mini-project-6f22d.appspot.com",
  "messagingSenderId": "1075887500553",
  "appId": "1:1075887500553:web:1d690a5bfb440cdb97b7d8",
  "measurementId": "G-RV6ZP2YGBL" ,
  "databaseURL":"https://final-mini-project-6f22d-default-rtdb.europe-west1.firebasedatabase.app/"
  }



firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('home'))
       except:
           error = "Authentication failed"
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        user={"email":request.form['email'], "password":request.form['password'], "full_name": request.form['full_name'], "username": request.form['username']}
        db.child("User").child(login_session['user']['localId']).set(user)
        return redirect(url_for('home'))
       except:
           error = "Authentication failed"
   return render_template("signup.html")

    

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        tweet={"text":request.form['text'], "title":request.form['title'] , "uid":login_session['user']['localId']}
        db.child("tweet").push(tweet)
        return redirect('/all_tweets')
    return render_template("add_tweet.html")


@app.route('/all_tweets', methods=['GET','POST'])
def all_tweets():
    if request.method == 'GET':
        tweet_dict=db.child("tweet").get().val()
    return render_template("tweets.html" , tweet_dict = tweet_dict)

@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        tweet={"text":request.form['text'], "title":request.form['title']}
        db.child("tweet").push(tweet)
        return redirect('/all_tweets')
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)


