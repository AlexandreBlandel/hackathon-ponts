from flask import Flask
from flask import render_template
from flask import request
from src.utils import ask_question_to_pdf
from random import randint


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


@app.route("/qcm")
def qcm():
    return render_template("qcm.html")


@app.route("/add_qcm", methods=["GET"])
def add_qcm():
    with open("qcm.txt", "w", encoding="utf_8") as file:
        file.write("")
    fact = ""
    dic = {}
    with open("qcm.txt", "a", encoding="utf_8") as file:
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
                answer = ask_question_to_pdf.ask_question_to_pdf(text_send)
            else:
                text_send = (
                    "Donne moi une réponse en une phrase courte, cette phrase doit contenir une affirmation vraie."
                    + Old_fact
                    + "De plus, cette affirmation vraie doit imperativement provenir de ce texte source:"
                )
                answer = ask_question_to_pdf.ask_question_to_pdf(text_send)
            fact += f"- " + answer + f"\n"
            dic[f"answer{i}"] = answer
            dic[f"{i}"] = k
    return dic


@app.route("/choix_pdf", methods=["GET", "POST"])
def choice_PDF():
    ask_question_to_pdf.change_PDF()
    return render_template("change.html")
