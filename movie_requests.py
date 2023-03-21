
#python -m venv env
#.\env\Scripts\activate
#pip install requests
#pip freeze > requirements.txt


import csv
import requests
from keys import api_key

def clean_box_office(input_box_office):
    box_office_split = input_box_office.split('$')[1].split(',')
    box_office_string =''.join(box_office_split)
    box_office_int = int(box_office_string)
    return box_office_int

def clean_award_wins(input_wins):
    wins_split = input_wins.split('wins')[0].split('.')[1]
    wins_int = int(wins_split)
    return wins_int

def clean_award_noms(input_noms):
    noms_split = input_noms.split('nominations')[0].split('&')[1]
    noms_int = int(noms_split)
    return noms_int

def clean_runtime(input_time):
    runtime_split = input_time.split(' ')[0]
    runtime_int = int(runtime_split)
    return runtime_int

def get_movie_data(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header row
        data = []
        for row in reader:
            title = row[0]
            imdb_id = row[1]
            url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                movie_data = response.json()
                data.append(movie_data)
    with open('movies.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Movie Title', 'Runtime', 'Genre', 'Award Wins', 'Award Nominations', 'Box Office'])
        for movie in data:
            writer.writerow([movie['Title'], clean_runtime(movie['Runtime']), movie['Genre'], clean_award_wins(movie['Awards']), clean_award_noms(movie['Awards']), clean_box_office(movie.get('BoxOffice', '0'))])

    return data

movie_data = get_movie_data('oscar_winners.csv')
