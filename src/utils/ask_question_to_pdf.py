from io import StringIO

import tkinter as tk
from tkinter import filedialog

import json

import os
import fitz
import openai
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize
from openai import OpenAI
from random import randint

load_dotenv()


def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()



openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")
texte = "Resume moi le texte ci dessous"
filesnom = "filename.pdf"


def read_pdf(filename):
    context = ""

    # Open the PDF file
    with fitz.open(filename) as pdf_file:
        # Get the number of pages in the PDF file
        num_pages = pdf_file.page_count

        # Loop through each page in the PDF file
        for page_num in range(num_pages):
            # Get the current page
            page = pdf_file[page_num]

            # Get the text from the current page
            page_text = page.get_text().replace("\n", "")

            # Append the text to context
            context += page_text
    return context


def split_text(text, chunk_size=5000):
    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence_size = len(sentence)
        if sentence_size > chunk_size:
            while sentence_size > chunk_size:
                chunk = sentence[:chunk_size]
                chunks.append(chunk)
                sentence = sentence[chunk_size:]
                sentence_size -= chunk_size
                current_chunk = StringIO()
                current_size = 0
        if current_size + sentence_size < chunk_size:
            current_chunk.write(sentence)
            current_size += sentence_size
        else:
            chunks.append(current_chunk.getvalue())
            current_chunk = StringIO()
            current_chunk.write(sentence)
            current_size = sentence_size
    if current_chunk:
        chunks.append(current_chunk.getvalue())
    return chunks


def gpt3_completion(text):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "system", "content": text}]
    )
    return response.choices[0].message.content


def ask_question_to_pdf(text=texte, files=filesnom):
    filename = os.path.join(os.path.dirname(__file__), files)
    document = read_pdf(filename)
    chunks = split_text(document)
    pdftext = ""
    for t in chunks:
        pdftext += t + f"{t}\n"
    return gpt3_completion(text + f"{text}\n\n{pdftext}" + pdftext)


def reset_prompt():
    with open("data/prompt.txt", "w", encoding="utf_8") as file:
        file.write("")


def add_prompt(text):
    with open("data/prompt.txt", "a", encoding="utf_8") as file:
        file.write(text)
    return None


def read_prompt():
    with open("data/prompt.txt", "r", encoding="utf_8") as file:
        chaine = ""
        for lignes in file:
            chaine += lignes
    return chaine


def compte_prompt(text):
    with open("data/prompt.txt", "r", encoding="utf_8") as file:
        lignes = file.readlines()
    return len(lignes)


def generate_qcm():

    with open("data/qcm.txt", "w", encoding="utf_8") as file:
        file.write("")
    fact = ""
    dic = {}
    with open("data/qcm.txt", "a", encoding="utf_8") as file:
        for i in range(4):
            if i == 0:
                Old_fact = ""
            else:
                Old_fact = (
                    "De plus, cette affirmation ne doit pas être directement lié aux affirmations suivantes :"
                    + fact
                )
            k = randint(0, 1)
            file.write(f"{k}")
            if k == 0:
                text_send = (
                    "Donne moi une réponse en une phrase courte, cette phrase doit contenir une affirmation fausse qui ne porte pas sur les compétences des ingenieurs."
                    + Old_fact
                    + "De plus, cette affirmation doit être facilement réfutable à partir de ce texte:"
                )
                answer = ask_question_to_pdf(text_send)
            else:
                text_send = (
                    "Donne moi une réponse en une phrase courte, cette phrase doit contenir une affirmation vraie."
                    + Old_fact
                    + "De plus, cette affirmation vraie doit imperativement provenir de ce texte source:"
                )
                answer = ask_question_to_pdf(text_send)
            fact += f"- " + answer + f"\n"
            dic[f"answer{i}"] = answer
            dic[f"{i}"] = k
    return dic


def initialize_button():
    with open("data/button_qcm.txt", "w", encoding="utf_8") as file:
        file.write("0000")


def update_button(i):
    with open("data/button_qcm.txt", "r", encoding="utf_8") as file:
        actual_button = (file.read()).strip()
    print(actual_button)
    with open("data/button_qcm.txt", "w", encoding="utf_8") as file:

        chaine = ""
        for j in range(4):
            if j == i:
                chaine += str(int(not (bool(int(actual_button[j])))))
            else:
                chaine += actual_button[j]
        file.write(chaine)


"""
# Ouvrir le fichier sélectionné avec l'application par défaut
if file_path:
    os.startfile(file_path)  # Sous Windows
"""

"""
# Ouvrir le fichier JSON et charger les données
with open("prompt.js", "r") as file:
    data = json.load(file)

# Récupérer le statut du bouton
button_status = data["change_PDF-button"]["is_active"]
if button_status:
    # Ouvrir fenetre dialogue

    # Créer la fenêtre Tkinter
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale

    # Ouvrir une boîte de dialogue pour sélectionner un fichier
    file_path = filedialog.askopenfilename()
    print(file_path)
"""




def change_PDF():
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale
    file_path = filedialog.askopenfilename()
    print(file_path)
    # global filesnom=file_path
    return None
