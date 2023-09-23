import pandas as pd
import sqlite3
import spacy

from scrap.db_init import initialize_database

DATABASE_PATH = "discord_bot/scrap/html.sqlite"

def extraction(message):
    nlp = spacy.load('de_core_news_sm')

    doc = nlp(message)

    nouns = [token.text for token in doc if token.pos_ == 'NOUN']
    entities = [ent.text for ent in doc.ents]

    df = initialize_database(DATABASE_PATH)

    outputs = []
    if not entities:
        print("NO ENTITYS FOUND")
        for noun in nouns:
            outputs = outputs + [text for text in df["text"] if noun in text][:5]
    else:
        for entity in entities:
            outputs = outputs + [text for text in df["text"] if entity in text][:5]
    return outputs