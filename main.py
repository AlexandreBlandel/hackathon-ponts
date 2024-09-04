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
        "Tu es un fier pirate, tu dois poser une question a un matelot sur ce texte "
    )
    # "Tu es un professeur et tu m'as demandé à apprendre le texte ci-dessous, pose donc une question sur un details précis pour t'assurer que le texte est bien su"
    ask_question_to_pdf.add_prompt(answer)
    return {"answer": f"{answer}"}


@app.route("/answer", methods=["POST"])
def reponse():
    prompt = request.form["prompt"]
    question = ask_question_to_pdf.read_prompt()
    texte_send = (
        "Voici la question qui m'a été posée :"
        + f"\n"
        + question
        + "Voici la réponse que j'ai donnée :"
        + f"\n"
        + prompt
        + "À partir du texte ci dessous, determine avec précision si la réponse donnée est juste ou non et, si elle ne l'est pas, donne la bonne réponse avec une explication claire"
    )
    answer = ask_question_to_pdf.ask_question_to_pdf(texte_send)
    ask_question_to_pdf.reset_prompt()
    return {"answer": f"{answer}"}
