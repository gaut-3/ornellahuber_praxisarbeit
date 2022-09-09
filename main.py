import os

import psycopg2
from flask import Flask, render_template, request, jsonify, session
from flask_login import login_required, login_user, LoginManager

from database.account_repository import load_account, insert_new_account, check_does_new_account_exist
from database.book_repository import load_all_ratings, insert_new_rating_user, load_user_ratings

conn = psycopg2.connect(
    host=os.environ.get('DATABASE_HOST', default='localhost'),
    port=os.environ.get('DATABASE_PORT', default='8888'),
    database="book-ratings-db",
    user="postgres",
    password="postgres")

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'N!tF42#9#ksL'

@app.route('/')
def start_page():
    return render_template('index.html')


@app.route('/new_rating')
def new_rating():
    if check_if_logged_in():
        return render_template('new_rating.html')
    else:
        return render_template('login.html')


@app.route('/ratings', methods=['GET'])
def load_ratings():
    if check_if_logged_in():
        username = session['username']
        books_with_ratings = load_user_ratings(username, conn)
        return render_template('ratings.html', book_ratings=books_with_ratings)
    else:
        return render_template('login.html')


@app.route('/ratings', methods=['POST'])
def create_new_rating():
    if check_if_logged_in():
        username = session['username']
        insert_new_rating_user(username, request.form['book_title'], request.form['rating'], conn)
        return render_template('new_rating_success.html', book_title=request.form['book_title'])
    else:
        return render_template('login.html')


def check_if_logged_in():
    if 'username' in session and session['username'] is not None:
        return True
    else:
        return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = load_account(request.form['username'], request.form['password'], conn)
        session['username'] = account.get("username")
        return render_template('profile.html', username=account.get("username"))
    if check_if_logged_in():
        return render_template('profile.html', username=session['username'])
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        exist = check_does_new_account_exist(request.form['username'], conn)
        if exist:
            return render_template('signup.html', error="Username exists")
        else:
            insert_new_account(request.form['username'], request.form['password'], conn)
            session['username'] = request.form['username']
            return render_template('profile.html', username=request.form['username'])
    if check_if_logged_in():
        return render_template('profile.html', username=session['username'])
    else:
        return render_template('signup.html', error=None)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.pop('username', None)
        return render_template('logout.html')


@login_manager.user_loader  
def load_user(account):
    
    return account


#### from here starts json API #######

@app.route('/api/ratings', methods=['GET'])
def load_ratings_for_api():
    books_with_ratings = load_all_ratings(conn)
    return jsonify(books_with_ratings)



@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
