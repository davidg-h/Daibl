from collections import Counter
import pandas as pd
import sqlite3
import spacy
import nltk
from nltk.tokenize import word_tokenize 
import numpy as np
from collections import Counter
from tqdm import tqdm  # Import tqdm for progress bar

from db_init import initialize_database

DATABASE_PATH = "discord_bot/scrap/html.sqlite"

from collections import Counter

def calculate_term_frequencies(tokens):
    term_count = Counter(tokens)
    total_terms = len(tokens)
    
    term_frequencies = {term: count / total_terms for term, count in term_count.items()}

    return term_frequencies


# Sample function to add a term frequency matrix column to the DataFrame
def add_term_frequency_column(df):
    df['term_frequency'] = df['tokens'].apply(calculate_term_frequencies)

def calculate_tfidf(df):
    n_docs = len(df)
    words_set = set(word for tokens in df['tokens'] for word in tokens)
    idf = {}

    for w in tqdm(words_set, desc="Calculating IDF", unit="word"):
        k = sum(1 for tokens in df['tokens'] if w in tokens)
        idf[w] = np.log10(n_docs / k)

    max_columns_per_table = 2000  # Adjust this value as needed
    num_subsets = len(df.columns) // max_columns_per_table + 1  # Calculate the number of subsets

    # Extract and store the 'term_frequency' column in a separate DataFrame
    term_frequency_df = df[['term_frequency']]

    # Create and load data into multiple databases
    for i in range(num_subsets):
        start_idx = i * max_columns_per_table
        end_idx = (i + 1) * max_columns_per_table if i < num_subsets - 1 else len(df.columns)
        columns_subset = df.columns[start_idx:end_idx]

        # Exclude 'term_frequency' column from the subsets (only include it in the first subset)
        if i == 0:
            df_tf_idf = df[['term_frequency'] + list(columns_subset)]
        else:
            df_tf_idf = df[list(columns_subset)]
            
        print(f"Subset {i+1}: Columns {start_idx + 1}-{end_idx}")
        
        database = f'html_db_{i+1}.sqlite'

        with sqlite3.connect(database) as con:
            # Store each subset in a separate table, append if it already exists
            table_name = f'tf_idf_subset_{i+1}'
            
            # Join the 'term_frequency' DataFrame with the subset DataFrame, specifying a suffix
            df_tf_idf = df_tf_idf.join(term_frequency_df, rsuffix='_term_frequency')
            
            # Remove the original 'term_frequency' column from the subset DataFrame
            df_tf_idf.drop(columns=['term_frequency'], inplace=True)

            df_tf_idf.to_sql(table_name, con, index=False, if_exists='append')
            
# Sample function to tokenize text
def tokenize_text(text):
    return word_tokenize(text.lower())

def extraction(message):
    nlp = spacy.load('de_core_news_sm')

    doc = nlp(message)

    nouns = [token.text for token in doc if token.pos_ == 'NOUN']
    entities = [ent.text for ent in doc.ents]

    df = initialize_database(DATABASE_PATH)
    
    # Tokenize the text and add a 'tokens' column to the DataFrame
    df['tokens'] = df['text'].apply(tokenize_text)

    # Calculate and add the term frequency matrix column
    add_term_frequency_column(df)
    calculate_tfidf(df)

    
    outputs = []
    if not entities:
        print("NO ENTITIES FOUND")
        for noun in nouns:
            outputs = outputs + [text for text in df["text"] if noun in text][:5]
    else:
        for entity in entities:
            outputs = outputs + [text for text in df["text"] if entity in text][:5]
    return outputs

extraction("wer ist Gallwitz")