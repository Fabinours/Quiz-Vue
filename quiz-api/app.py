from flask import Flask, request

from services.auth import AuthService
from entities.questions import QuestionEntity
from database import *
from json import dumps

app = Flask(__name__)

@app.route('/')
def hello_world():
	return "Hello, world"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def Login():
	payload = request.get_json()
	return AuthService().buildToken(payload["password"])
	
@app.route('/questions/<id>', methods=['GET'])
def GetQuestion(id):

	#Ajouter la question à la base de données
	db = Database()

	#Création de la question
	if QuestionEntity.exists(db, id):
		json = QuestionEntity.get(db, id).toJson()
		
		db.close()
		return json, 200

	#La position est déjà utilisée
	db.close()
	return 'The question does not exists!', 404 

@app.route('/questions', methods=['GET'])
def GetAllQuestions():

	#Ajouter la question à la base de données
	db = Database()

	#Création de la question
	questions_data = QuestionEntity.getAll(db)
	questions_data = list(map(lambda obj: obj.toJson(), questions_data))
	json = dumps(questions_data)
	
	db.close()
	return json, 200
	
@app.route('/questions', methods=['POST'])
def CreateQuestion():

	if not AuthService().isAuthentificated():
		return '', 401

	#Récupérer les données envoyées
	payload = request.get_json()

	#Ajouter la question à la base de données
	db = Database()
	
	#Création de la question
	created = QuestionEntity(payload["title"], payload["text"], payload["image"], payload["position"]).create(db)

	if created:
		db.close()
		return str(created), 200

	db.close()
	return 'Invalid position', 404

@app.route('/questions/<id>', methods=['PUT'])
def UpdateQuestion(id):
	
	if not AuthService().isAuthentificated():
		return '', 401

	#Récupérer les données envoyées
	payload = request.get_json()

	#Supprimer la question de la base de données
	db = Database()

	if QuestionEntity.exists(db, id):
		question = QuestionEntity(payload["title"], payload["text"], payload["image"], payload["position"])
		updated = question.update(db, id)

		if updated:
			db.close()
			return '', 200

		db.close()
		return 'Invalid position', 404

	#Retourner la réponse
	db.close()
	return 'Question does not exists', 404

@app.route('/questions/<id>', methods=['DELETE'])
def DeleteQuestion(id):
	
	if not AuthService().isAuthentificated():
		return '', 401

	#Supprimer la question de la base de données
	db = Database()

	if QuestionEntity.exists(db, id):
		QuestionEntity.delete(db, id)
		db.close()
		return '', 204

	#Retourner la réponse
	db.close()
	return 'Question does not exits', 404 

if __name__ == "__main__":
    app.run(ssl_context='adhoc', use_reloader=True, debug=True)