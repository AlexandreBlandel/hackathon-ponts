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
        "Tu dois desormais me poser une courte question pour verifier que je connais bien ce texte:"
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
        "À partir du texte ci-dessous et uniquement avec le texte détermine si la réponse "
        "donnée est correcte ou non et, si elle ne l'est pas, donne la bonne "
        "réponse avec une explication claire"
        "Et si elle est correcte felicite moi" 
        "Tu dois effectuer ta réponse en parlant comme le plus grand pirate."
    )
    answer = ask_question_to_pdf.ask_question_to_pdf(texte_send)
    ask_question_to_pdf.reset_prompt()
    return {"answer": f"{answer}"}


@app.route("/qcm")
def qcm():
    return render_template("qcm.html")


@app.route("/add_qcm", methods=["GET"])
def add_qcm():
    dic = ask_question_to_pdf.generate_qcm()
    ask_question_to_pdf.initialize_button()
    return dic


@app.route("/update_qcm", methods=["POST"])
def update_qcm():
    if request.method == "POST":
        dic = {}
        button = int(request.form["button"])
        ask_question_to_pdf.update_button(button)
        return dic


@app.route("/solution_qcm")
def solution_qcm():
    return render_template("reponse_qcm.html")


@app.route("/get_aide_qcm", methods=["GET"])
def get_aide_qcm():
    text = ask_question_to_pdf.result()
    dic = {}
    dic["answer"] = text
    return dic


@app.route("/choix_pdf")
def choice_PDF():
    print("Verification 0")
    ask_question_to_pdf.change_PDF()
    return None


# render_template("change.html")

"""
# Route pour la page d'upload
@app.route("/")
def index():
    return render_template("index.html")  # Ta page HTML avec le formulaire


# Route pour traiter les fichiers envoyés
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file-upload" not in request.files:
        return "Aucun fichier sélectionné"

    file = request.files["file-upload"]
    print(file)
    if file.filename == "":
        return "Pas de fichier sélectionné"

    # Sauvegarder le fichier dans le dossier uploads
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
    return f"Fichier {file.filename} envoyé avec succès!"
    """
