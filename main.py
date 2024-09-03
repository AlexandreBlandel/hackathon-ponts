from flask import Flask
from flask import render_template
from flask import request
from src.utils import ask_question_to_pdf


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



@app.route("/hello")
def hello():
    return render_template('index.html')


@app.route("/prompt",methods=['POST', 'GET'])
def prompt():
    if request.method == 'POST':
        prompt = request.form['prompt']
        answer = ask_question_to_pdf.ask_question_to_pdf(prompt)
        return {"answer" : f"{answer}"}
