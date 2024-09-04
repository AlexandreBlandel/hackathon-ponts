from flask import Flask
from flask import render_template
from flask import request
from src.utils import ask_question_to_pdf


app = Flask(__name__)


@app.route("/")
def hello_world():
    ask_question_to_pdf.reset_prompt()
    return render_template("acceuil.html")


@app.route("/hello")
def hello():
    return render_template("index.html")


@app.route("/prompt", methods=["POST"])
def prompt():
    if request.method == "POST":
        prompt = request.form["prompt"]
        answer = ask_question_to_pdf.ask_question_to_pdf(prompt)
        return {"answer": f"{answer}"}


@app.route("/question", methods=["GET"])
def question():
    answer = ask_question_to_pdf.ask_question_to_pdf(
        "Tu es mon professeur, pose moi une question sur le texte"
    )
    ask_question_to_pdf.add_prompt(answer)
    return {"answer": f"{answer}"}


@app.route("/answer", methods=["POST"])
def reponse():
    prompt = request.form["prompt"]
    question = ask_question_to_pdf.read_prompt()
    texte_send = (
        f"Voici la question qui m'a été posée :\n{question}"
        f"Voici la réponse que j'ai donnée :\n{prompt}"
        "À partir du texte ci-dessous, détermine avec précision si la réponse "
        "donnée est juste ou non et, si elle ne l'est pas, donne la bonne "
        "réponse avec une explication claire."
    )
    answer = ask_question_to_pdf.ask_question_to_pdf(texte_send)
    ask_question_to_pdf.reset_prompt()
    return {"answer": f"{answer}"}
