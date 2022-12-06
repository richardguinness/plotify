import numpy as np
import pandas as pd
import re

#breakpoint()
## IMPORT DATA

# books
books = pd.read_csv('Datasets/Cleaned_Books.csv')
books = pd.DataFrame(books).rename(columns = {'BookTitle': 'Title'}).drop(columns = ['Unnamed: 0', 'Index', 'ID','Summary Length','Genre Count','Author'])

# movies
movies = pd.read_csv('Datasets/mpst_full_data.csv')
movies = pd.DataFrame(movies).rename(columns={'title': 'Title', 'plot_synopsis': 'Summary', 'tags': 'Genres'}).drop(columns = ['imdb_id', 'split', 'synopsis_source'])

# combine datasets
books_movies = pd.concat([books, movies], ignore_index=True)



## CLEAN DATA

def preprocess_text(text):
    text = text.lower()  # Lowercase text
    text = text.strip("""""")  # Remove punctuation
    text = text.replace("'", '')
    text = text.replace('"', '')
    text = text.strip('[]')
    text = text.replace(', ', ',')
    text = " ".join(text.split())  # Remove extra spaces, tabs, and new lines
    return text.split(",") #list(text.split(", "))

books_movies["Genres"] = books_movies["Genres"].map(preprocess_text)



## INPUT FIRST RECOGNISED GENRE FROM GENRE LISTS

split_genres = pd.DataFrame(books_movies["Genres"].tolist()).fillna('z')

# basic list based on the top 30 genres by count
valid_genres = ['murder','violence', 'crime fiction', 'gothic',
                'speculative fiction','fantasy', 'science fiction', 'sci-fi','alternate reality',
                'romantic', 'romance novel', 'romantic, comedy',
                'suspenseful', 'suspense','mystery','revenge', 'tragedy', 'detective fiction',
                'novel', 'historical novel',
                'childrens literature', 'young adult literature',
                'comedy', 'satire', 'humor', 'entertaining','prank',
                'horror', 'tragedy', 'dark','sadist', 'cult', 'psychedelic', 'insanity', 'cruelty','paranormal',
                'action', 'neo noir', 'thriller', 'dramatic', 'adventure novel']


# go through all genres by column and reassign with the genre label that appears in the valid_genres list
tmp_list = []
for j in range(0,24):
    tmp_list.append(split_genres[j].apply(lambda x: ', '.join([i for i in valid_genres if i in x])))

# concat all the valid genres into one column and replace helper blanks with NANs, return first in new list that is not NaN
valid_genre_df = pd.concat(tmp_list, axis=1).replace(r'^\s*$', np.nan, regex=True).fillna(method='bfill', axis=1).iloc[:, 0]

# concat updated list of genres with original book list
books_movies_genre = pd.concat([books_movies, valid_genre_df],axis=1).rename(columns={0:"Genre_new"})



## REPLACE GENRES WITH GENRE CATEGORY

# dictionary with genres
valid_genres_dict = {'Crime': ['murder','violence', 'crime fiction', 'gothic'],
                'Fantasy': ['speculative fiction','fantasy', 'science fiction', 'sci-fi','alternate reality'],
                'Romance': ['romantic', 'romance novel', 'romance novel, novel', 'romantic, comedy'],
                'Mystery': ['suspenseful', 'suspense','mystery', 'suspenseful, suspense','revenge', 'tragedy', 'detective fiction'],
                'Novel': ['novel', 'historical novel', 'novel, historical novel'],
                'Childrens Literature': ['childrens literature','young adult literature'],
                'Comedy': ['comedy', 'satire', 'humor', 'entertaining','prank'],
                'Horror': ['horror', 'tragedy', 'dark','sadist', 'cult', 'psychedelic', 'insanity', 'cruelty','paranormal'],
                'Action': ['action', 'neo noir', 'thriller', 'dramatic', 'adventure novel']}


# function to lookup an item in a dictionary values list, and return the dictionary key

def return_genre_cat(x):
    results = [k if x == v or x in v else None for k, v in valid_genres_dict.items()]
    tmp_result = [i for i in results if i is not None]
    tmp_result = tmp_result[0] if len(tmp_result) > 0 else np.nan
    return tmp_result


# replace the specific genres with genre category
books_movies_genre['Genre_Grp'] = books_movies_genre['Genre_new'].apply(return_genre_cat)


## Clean Summary Text

# function to clean the summary text
def clean_text(text):
    """
    - remove any html tags (< /br> often found)
    - Keep only ASCII + Latin chars, digits and whitespaces
    - pad punctuation chars with whitespace
    - convert all whitespaces (tabs etc.) to single wspace
    """
    RE_PUNCTUATION = re.compile("([!?.,;-])")
    RE_TAGS = re.compile(r"<[^>]+>")
    RE_ASCII = re.compile(r"[^A-Za-zÀ-ž,.!?0-9 ]", re.IGNORECASE)
    RE_WSPACE = re.compile(r"\s+", re.IGNORECASE)
    text = re.sub(RE_TAGS, " ", text)
    text = re.sub(RE_ASCII, " ", text)
    text = re.sub(RE_PUNCTUATION, r" \1 ", text)
    text = re.sub(RE_WSPACE, " ", text)
    return text


# Clean Comments. Only keep long enough
books_movies_genre['Summary_clean'] = books_movies_genre.loc[books_movies_genre['Summary'].str.len() > 10, "Summary"]
books_movies_genre['Summary_clean'] = books_movies_genre["Summary_clean"].apply(clean_text)
books_movies_genre_short = books_movies_genre[books_movies_genre["Summary_clean"].str.len() <=3000]


# drop blank genres
books_movies_genre_short = books_movies_genre_short.dropna(how = 'all', subset='Genre_new')


## PUSH TO CSV

books_movies_genre_short[['Title', 'Summary_clean', 'Genre_Grp']].to_csv("Datasets/book_movies_final.csv", index=False)
