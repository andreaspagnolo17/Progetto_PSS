from flask import render_template, request
from model import recommend, provider_mapping, movies
import pandas as pd

def get_recommendations():
    # La lista dei film
    available_movies = movies['title'].tolist()

    # Se viene fatto un POST (quando l'utente preme "Consiglia")
    if request.method == 'POST':
        selected_movie_name = request.form.get('movie')
        selected_platforms = request.form.getlist('platforms')
        
        # Mappare le piattaforme ai loro ID
        selected_provider_ids = [provider_mapping[platform] for platform in selected_platforms if platform in provider_mapping]

        # Ottenere i nomi, poster e link dei film consigliati
        names, posters, links = recommend(selected_movie_name, selected_provider_ids)

        return render_template('index.html', names=names, posters=posters, links=links, selected_movie_name=selected_movie_name, movies=available_movies, selected_platforms=selected_platforms)
    
    # Se non c'è stato un POST (prima che l'utente selezioni qualcosa), restituisci la pagina con la lista dei film
    return render_template('index.html', names=None, movies=available_movies, selected_platforms=[])