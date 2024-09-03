from io import StringIO
import os
import fitz
import openai
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize
from openai import OpenAI

load_dotenv()


def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")


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
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": text}
        ]
    )
    return response.choices[0].message.content

def ask_question_to_pdf(text=f"Resume moi le texte ci dessous",files = "filename.pdf"):
    filename = os.path.join(os.path.dirname(__file__), files)
    document = read_pdf(filename)
    chunks = split_text(document)
    pdftext = ""
    for t in chunks:
        pdftext += t + f"\n"
    return gpt3_completion(text + f"\n\n" + pdftext)


def add_prompt(text):
    with open("prompt.txt","a",encoding="utf_8") as file:
        file.write(text)
    return None

def read_prompt(text):
    with open("prompt.txt","r",encoding="utf_8") as file:
        chaine=f""
        for lignes in file :
            ligne=lignes.strip()
            chaine+=f"\n"+ligne
    return chaine

