import pandas as pd
import pickle
import requests

# TMDb API Key
API_KEY = '9aba39119c399b5f3985ab6825be0aff'

# Carica i dati delle piattaforme di streaming dal CSV
providers_movies_df = pd.read_csv('data/providers_movies.csv')

# Carica i dati dei film e la matrice di similarità
movies_dict = pickle.load(open('data/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('data/similarity.pkl', 'rb'))

# Mappatura dei provider
provider_mapping = {
    'Netflix': 8,
    'Disney+': 337,
    'Amazon Prime': 119,
    'Apple tv': 2,
    'Tim vision': 109
}

# Funzione per ottenere il poster del film e il link alla scheda del film su TMDb
def fetch_poster_and_link(movie_id):
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US")
        response.raise_for_status()
        data = response.json()
        poster_url = f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        movie_link = f"https://www.themoviedb.org/movie/{movie_id}"
        return poster_url, movie_link
    except requests.exceptions.RequestException as e:
        print(f"Errore nel recupero del poster e del link per il film ID {movie_id}: {e}")
        return None, None

# Funzione per ottenere i film disponibili su una o più piattaforme
def get_movies_by_providers_cached(provider_ids):
    if not provider_ids:
        return set()  # Se non ci sono piattaforme selezionate, non fare alcun filtro
    
    filtered_df = providers_movies_df[providers_movies_df['Provider'].isin([k for k, v in provider_mapping.items() if v in provider_ids])]
    return set(filtered_df['Movie ID'].unique())

# Funzione di raccomandazione
def recommend(movie, provider_ids=None):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:]  # Esclude il film stesso
    
    if provider_ids:
        platform_movie_ids = get_movies_by_providers_cached(provider_ids)
    else:
        platform_movie_ids = set()  # Nessun filtro se non è specificato il provider
    
    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_links = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        if not provider_ids or movie_id in platform_movie_ids:
            poster, link = fetch_poster_and_link(movie_id)
            if poster and link:
                recommended_movies.append(movies.iloc[i[0]].title)
                recommended_movies_posters.append(poster)
                recommended_movies_links.append(link)
                if len(recommended_movies) == 5:
                    break

    return recommended_movies, recommended_movies_posters, recommended_movies_links