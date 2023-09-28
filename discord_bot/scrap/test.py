from transformers import BertTokenizer, BertModel
import torch
import sqlite3
import pandas as pd
from scipy.spatial.distance import cosine
from db_init import initialize_database


# Lade den BERT-Tokenizer und das Modell
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Annahme: Sie haben Ihre Datenbankverbindung und den DataFrame bereits initialisiert
database_path = "daibl-1\discord_bot\scrap\html.sqlite"

# Initialisiere den DataFrame mit der Funktion aus db_init.py
html_df = initialize_database(database_path)


# Initialisiere eine leere Liste, um Embeddings für alle Dokumente zu speichern
document_embeddings = []

# Iteriere über alle Dokumente im DataFrame
for document_text in html_df["text"]:
    # Tokenisierung der Frage und des Dokuments
    tokens_document = tokenizer.tokenize(document_text)

    # Konvertiere Tokens in IDs
    token_ids_document = tokenizer.convert_tokens_to_ids(tokens_document)

    # Erstelle Tensoren für die Eingabe
    tokens_tensor_document = torch.tensor([token_ids_document])
    segments_tensor_document = torch.tensor([[1] * len(token_ids_document)])

    # Berechne Embeddings für das Dokument
    with torch.no_grad():
        outputs_document = model(tokens_tensor_document, segments_tensor_document)
        hidden_states_document = outputs_document[2]

    # Erstelle Durchschnittseinbettungen für Frage und Dokument
    sentence_embedding_question = torch.mean(token_vecs_question, dim=0)
    
    token_vecs_document = hidden_states_document[-2][0]
    sentence_embedding_document = torch.mean(token_vecs_document, dim=0)

    # Berechne den Kosinus-Abstand zwischen Frage- und Dokument-Einbettungen
    similarity = 1 - cosine(sentence_embedding_question, sentence_embedding_document)
    
    # Füge das Dokument und die Ähnlichkeit zur Liste hinzu
    document_embeddings.append((document_text, similarity))

# Sortiere die Dokumente nach Ähnlichkeit
document_embeddings.sort(key=lambda x: x[1], reverse=True)

# Gib die sortierten Dokumente und ihre Ähnlichkeiten aus
for document, similarity in document_embeddings:
    print(f"Dokument: {document}")
    print(f"Ähnlichkeit: {similarity:.4f}")
    print("=" * 50)
