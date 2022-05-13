from flask import Flask, request
from jwt_utils import *
from questions import *
from database import *

app = Flask(__name__)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def Login():
	payload = request.get_json()
	#Verify password in payload
	if(payload["password"] == "Vive l'ESIEE !"):
		return {"token": build_token()}, 200
	else:
		return '', 401
	
@app.route('/questions', methods=['POST'])
def CreateQuestion():
	#Récupérer le token envoyé en paramètre
	token = request.headers.get('Authorization').split(' ')[1]
	try:
		#Vérifier que le token est valide
		decode_token(token)

		#Récupérer les données envoyées
		payload = request.get_json()
		question = Question(payload["title"], payload["text"], payload["image"])

		#Ajouter la question à la base de données
		conn = create_connection()
		result = create_question(conn, question)
		conn.close()

		print(result)

		#Retourner la réponse
		return '', 200
	except BaseException as err:
		return f'{err}', 401

if __name__ == "__main__":
    app.run(ssl_context='adhoc')