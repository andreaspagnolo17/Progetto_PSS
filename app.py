from flask import Flask, render_template, redirect, url_for, session
from controller import get_recommendations
from model import movies, fetch_poster_and_link

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session

# Initialize watchlist in session if not exists
@app.before_request
def initialize_watchlist():
    if 'watchlist' not in session:
        session['watchlist'] = []

@app.route('/', methods=['GET', 'POST'])
def index():
    return get_recommendations()

@app.route('/add_to_watchlist/<movie_name>')
def add_to_watchlist(movie_name):
    if movie_name not in session['watchlist']:
        session['watchlist'].append(movie_name)
        session.modified = True
    return redirect(url_for('index'))

@app.route('/remove_from_watchlist/<movie_name>')
def remove_from_watchlist(movie_name):
    if movie_name in session['watchlist']:
        session['watchlist'].remove(movie_name)
        session.modified = True
    return redirect(url_for('personal_area'))

@app.route('/personal_area')
def personal_area():
    watchlist_movies = []
    for movie_name in session.get('watchlist', []):
        # Trova l'ID del film nel dataframe
        movie_row = movies[movies['title'] == movie_name]
        if not movie_row.empty:
            movie_id = movie_row.iloc[0]['movie_id']
            poster, link = fetch_poster_and_link(movie_id)  # Ora otteniamo anche il link
            watchlist_movies.append({
                'name': movie_name,
                'poster': poster if poster else None,
                'tmdb_link': link if link else '#'  # Aggiungi il link TMDb
            })
    
    return render_template('personal_area.html', watchlist=watchlist_movies)

if __name__ == '__main__':
    app.run(debug=True)