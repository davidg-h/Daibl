import json
import os

import requests
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
from tqdm import tqdm

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


def get_sample_answer(question):
    if question == "Wie ist die Email Adresse von Professor Gallwitz?":
        return "Die Email Adresse von Prof. Dr. Gallwitz ist: florian.gallwitz@th-nuernberg.de"
    elif question == "Was soll ich beachten, wenn ich eine Prüfung anmelden will?":
        return "Um eine Prüfung anzumelden, müssen Sie folgende Kriterien beachten: Anmeldefristen,Zulassungsvoraussetzungen, Anmeldeverfahren, Prüfungstermin, Prüfungsvorbereitung."
    elif (
        question
        == "Welche voraussetzungen, muss ich für den Master Studiengang erfüllen?"
    ):
        return "Für den MIN Master Studiengang an der Technische Hochschule Nürnberg , müssen Sie folgende Voraussetzungen erfüllen: Bachelorabschluss in IN/MIN/WIN oder verwandete Fächer, Notendurchschnitt von 2,5, Sprachkenntnisse von C1, Bewerbungsunterlagen bereit stellen."
    elif question == "Welche Professoren gibt es an der Fakultät Soziale Arbeit?":
        return "An der Fakultät für Soziale Arbeit gibt es folgende Proffessoren: Johannes Bach, Steffen Brockmann, Michael Domes, Simone Emmert, Carolin Freier, Sabine Fromm …"
    elif question == "Wann und was muss ich im IT-Projekt machen?":
        return "Der Praxisbeauftragter der Fakultät Informatik ist Prof. Dr. Wolfgang Bremer."


def gpt_evaluate_outputs(df):
    client = OpenAI(api_key=API_KEY)
    scores = []
    reasons = []
    for row in tqdm(df.iterrows()):
        row = row[1]
        question = row["Question"]
        sample_answer = get_sample_answer(question)
        model_answer = row["Response"]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": """
                    Du bewertest Ausgaben eines Retrieval Augmented Gerneration Systems, das Fragen von Studenten zum Studium an der Technische Hochschule Nürnberg Georg Simon Ohm beantwortet.
                    Bewerte dabei folgende Kriterien und vergebe Punkte. 
                    Inhaltliche Korrektheit: die Ausgabe enthält die richtige Antwort (0-4)
                    Sprachliche Gestaltung: die Ausgabe enthält grammatikalisch richtige Sätze und eine logische Struktur (0-3)
                    Fokus: die Ausgabe enthält keine anderen unrelevanten Informationen (0-3)

                    Ziehe anschließend ein Fazit und bewerte das Ergebnis mit einer Punktzahl
                    Antworte in JSON Format mit einer 'Begründung' und einem 'Score'""",
                },
                {
                    "role": "user",
                    "content": f"""
                        Frage: {question}
                        Beispielantwort: {sample_answer}
                        Antwort RAG: {model_answer}
                    """
                }
            ]
        )
        try:
            content = json.loads(response.choices[0].message.content)
            reason = content["Score"]
            score = content["Score"]
            reasons.append(reason)
            scores.append(score)
        except:
            reasons.append("-1")
            scores.append("-1")
            print("Answer not in right format")

    df["Begründung"] = reasons
    df["Score"] = scores
    return df





# gpt_sosrt()
