from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import spacy

app = Flask(__name__)
#
# creating an API object
api = Api(app)
nlp = spacy.load("ai_spacy/output1/model-best")


@app.route("/prediction", methods=["GET", "POST"])
def get_prediction():
    data = request.data.decode()
    print(data)
    doc = nlp(data)
    dect = []
    for ent in doc.ents:
        dect.append((ent.label_, ent.text))
    print(dect)
    r = jsonify(dect)
    r.headers.add('Access-Control-Allow-Origin', '*')
    r.headers.add('Access-Control-Allow-Header', '*')
    return r


if __name__ == '__main__':  # ngrok http 5000
    app.run(debug=True)
