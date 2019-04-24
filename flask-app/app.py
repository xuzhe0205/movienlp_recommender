from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Movies
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


app = Flask(__name__)
mysql = MySQL()
# Config MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'oliverxu'
app.config['MYSQL_DATABASE_PASSWORD'] = 'xuzhe950205'
app.config['MYSQL_DATABASE_DB'] = 'myflaskapp'
# make sure the data returned from the mysql database is not a tuple but a dictionary
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL


mysql.init_app(app)

Movies = Movies()
#Main page
@app.route('/')
def index():
    return render_template('home.html')
#About
@app.route('/about')
def about():
    return render_template('about.html')
#Movies
@app.route('/mymovies')
def mymovies():
    return render_template('mymovies.html', movies = Movies)
# Movie
@app.route('/movie/<string:id>/')
def mymovie(id):
    # Create cursor
    conn = mysql.connect()
    df_ratings = pd.read_sql('SELECT * FROM ratings', con = conn)
    df_movies = pd.read_sql('SELECT * FROM movies', con = conn)
    df_ratings_pivot = df_ratings.pivot(
        index='movieId',
        columns='userId',
        values='rating'
    ).fillna(0)
    movie_rating_train = csr_matrix(df_ratings_pivot.values)
    movie_neighbors = NearestNeighbors(metric='cosine', algorithm='brute')
    movie_neighbors.fit(movie_rating_train)
    query_index = int(id)
    print('hahahahha',query_index)
    distances, indices = movie_neighbors.kneighbors(df_ratings_pivot.loc[df_ratings_pivot.index == query_index].values.reshape(1,-1), n_neighbors = 6)
    recommend_list = []

    for i in range(len(distances.flatten())):
        if i == 0:
            pass
            # print('Recommendations for {0}:\n'.format(df_movies.loc[df_movies['movieId']==df_ratings_pivot.index[query_index], 'title'].iloc[0]))
        else:
            recommend_list.append(df_ratings_pivot.index[indices.flatten()[i]])
            # print ('{0}:{1}, with distance of {2}:'.format(i, df_ratings_pivot.index[indices.flatten()[i]], distances.flatten()[i]))
    
    recommend_res = pd.DataFrame(recommend_list, columns=['movieId'])
    recommend_res = pd.merge(recommend_res, df_movies, on='movieId')
    column_names = recommend_res.columns
    data_dict = [dict(zip(column_names, row))  
            for row in recommend_res.values]
    df_query_movie = df_movies.loc[df_movies['movieId'] == query_index]
    movie = df_query_movie.to_dict('records')[0]
    
    return render_template('movie.html', query_movie = movie, movies = data_dict)


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username  = StringField('Username', [validators.Length(min=4, max=50)])
    email = StringField('Email',  [validators.Length(min=6, max=50)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match bro :(')
    ])
    confirm = PasswordField('Confirm Password')
# it will accept get and post
@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        # need to encrypt here
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor, and use cur to execute command (mysql query)
        conn = mysql.connect()
        cur = conn.cursor()

        # Execute sql query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
        # Commit to DB
        conn.commit()
        # Cerrar conexion
        cur.close()


        flash('You are now registered and can log in', 'suceess')

        redirect(url_for('index'))
    return render_template('register.html', form = form)

#login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        conn = mysql.connect()
        cur = conn.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s",[username])
        #if there is any row found
        if result > 0:
            # get stored hash
            data = cur.fetchone()
            user_id, name, email, username, password = data
            # password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate,password):
                app.logger.info('PASSWORD MATCHED')
                # If succeed, pass in session variable
                session['logged_in'] = True
                session['username'] = username

                flash('Logged in! Welcome to movie world!', 'success')
                return redirect(url_for('dashboard'))
            else:
                app.logger.info('PASSWORD NOT MATCHED')
                error = 'Invalid login'
                return render_template('login.html', error=error)
            
            # Close connection
            cur.close()
                
        else:
            app.logger.info('NO USER')
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login','danger')
            return redirect(url_for('login'))
    return wrap

def get_random_movies():
    # Create cursor, and use cur to execute command (mysql query)
    conn = mysql.connect()
    cur = conn.cursor()

    # Execute sql query
    random_movies = cur.execute("SELECT * FROM movies ORDER BY RAND() LIMIT 30")

    data = cur.fetchall()

    desc = cur.description
    column_names = [col[0] for col in desc]
    data_dict = [dict(zip(column_names, row))  
            for row in data]
    
    # Close cursor
    cur.close()
    return data_dict



# logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out, bye bye', 'success')
    return redirect(url_for('login'))


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    random_movies = get_random_movies()
    print('?????????')
    return render_template('dashboard.html',movies = random_movies)


# Search
@app.route('/search_movie', methods = ['GET', 'POST'])
@is_logged_in
def search():
    print('????????wocao!!?')
    if request.method=="POST":
        print('????????hahahah!!!?')
        movie_name = request.form['query_movie']
        print('what is this: ', movie_name)
        # Create cursor
        conn = mysql.connect()
        cur = conn.cursor()
        query_movies = cur.execute("SELECT * FROM movies WHERE movies.title LIKE %s", ['%'+movie_name+'%'])
        data = cur.fetchall()
        desc = cur.description
        column_names = [col[0] for col in desc]
        movie_dict = [dict(zip(column_names, row))  
                for row in data]

        # Close cursor
        cur.close()
        print('????????!!!?')
        print('lalallalallaal', query_movies)
        return render_template('search_movie.html', movies = movie_dict)
    return render_template('search_movie.html')

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)