from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyBmklFjoEhTj0lflN4adVPTEoqn0rGzNiA",
  "authDomain": "lab-project-c97d8.firebaseapp.com",
  "projectId": "lab-project-c97d8",
  "storageBucket": "lab-project-c97d8.appspot.com",
  "messagingSenderId": "963828519606",
  "appId": "1:963828519606:web:88a90689dc19876e7a0c17",
  "measurementId": "G-1YSQ8FSTWK",
  "databaseURL": "https://lab-project-c97d8-default-rtdb.asia-southeast1.firebasedatabase.app/"
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
        return redirect(url_for('add_tweet'))
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
        user={"email":request.form['email'], "password":request.form['password'], "full_name": request.form['full_name'], "username": request.form['username'], "bio": request.form['bio']}
        db.child("User").child(login_session['user']['localId']).set(user)
        return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
   return render_template("signup.html")

    

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        tweet={"text":request.form['text'], "title":request.form['title'] , "uid":login_session['user']['localId']}
        db.child("tweet").push(tweet)
    return render_template("add_tweet.html")


@app.rout('/all_tweets')
def all_tweets():
    if request.method == 'POST':
        print(db.child(tweets).child(login_session)['user']['localId']).get().val()
    return render_template("all_tweet.html")

if __name__ == '__main__':
    app.run(debug=True)


