# import json
from re import M
from authy.api import AuthyApiClient
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,Response
from requests.sessions import session
from werkzeug.wrappers import response
from flask_cors import CORS

from chat import get_response


app = Flask(__name__)
CORS(app)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

api = AuthyApiClient(app.config['AUTHY_API_KEY'])

@app.route("/", methods=['GET', 'POST'])
def index_get():
    return render_template('base.html')

@app.post('/predict')
def predict():
    text = request.json.get("message")
    #check if response is valid
    response = get_response(text)
    #   response.headers.add('Access-Control-Allow-Origin', '*')
    message = {"answer": response}
    return jsonify(message)

@app.route("/phone_verification", methods=["GET", "POST"])
def phone_verification():
    if request.method == "POST":
        phone_number = request.form.get("phone_number")
        country_code = request.form.get("country_code")
        method = request.form.get("method")
        api.phones.verification_start(phone_number,country_code,via=method)

        return redirect(url_for('verify', phone_number=phone_number, country_code=country_code))
           
    return render_template("phone_verification.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        token = request.form.get("token")
        phone_number = request.form.get("phone_number")
        country_code = request.form.get("country_code")
        verification = api.phones.verification_check(phone_number,country_code,token)

        if verification.ok():
            return Response("<h1>Success!</h1>")

    return render_template("verify.html")

if __name__ == '__main__':
    app.run()

