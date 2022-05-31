from flask import Flask, request
from flask_cors import CORS
from entities.answers import AnswerEntity

from services.auth import AuthService
from entities.questions import QuestionEntity
from entities.participations import ParticipationEntity
from database import *
from json import dumps

app = Flask(__name__)
CORS(app)

###> GENERAL <###
@app.route('/')
def hello_world():
	return "Hello, world"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	#Récupérer la base de données
	db = Database()

	return {
		"size": len(QuestionEntity.getAll(db)), 
		"scores": list(map(lambda el : el.toJson(), ParticipationEntity.getAll(db)))
	}, 200

@app.route('/login', methods=['POST'])
def Login():
	print("login")
	payload = request.get_json()
	return AuthService().buildToken(payload["password"])
	
###> QUESTION <###
@app.route('/questions/<position>', methods=['GET'])
def GetQuestion(position):

	#Ajouter la question à la base de données
	db = Database()

	#Création de la question
	question = QuestionEntity.getByPosition(db, position)
	if question:
		json = question.toJson()
		
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
	questions_data = list(map(lambda obj: obj.toJson(), QuestionEntity.getAll(db)))
	
	db.close()
	return { "questions" : questions_data }, 200
	
@app.route('/questions', methods=['POST'])
def CreateQuestion():

	if not AuthService().isAuthentificated():
		return 'Bad auth', 401

	#Récupérer les données envoyées
	payload = request.get_json()

	#Ajouter la question à la base de données
	db = Database()
	
	#Création de la question
	questionEntity = QuestionEntity(payload["title"], payload["text"], payload["image"], payload["position"])
	possibleAnswers = list(map(lambda json: AnswerEntity.fromJson(json), payload["possibleAnswers"]))
	questionEntity.setPossibleAnswers(possibleAnswers)
	
	created = questionEntity.create(db)
	
	if created:
		db.close()
		return str(created), 200
		
	db.close()
	return 'Invalid position', 404

@app.route('/questions/<position>', methods=['PUT'])
def UpdateQuestion(position):
	
	if not AuthService().isAuthentificated():
		return 'Bad auth', 401

	#Récupérer les données envoyées
	payload = request.get_json()

	#Supprimer la question de la base de données
	db = Database()

	questionEntity = QuestionEntity.getByPosition(db, position)
	if questionEntity:

		questionEntity.title, questionEntity.text = payload["title"], payload["text"]
		questionEntity.image, questionEntity.position = payload["image"], payload["position"]
		possibleAnswers = list(map(lambda json: AnswerEntity.fromJson(json), payload["possibleAnswers"]))
		questionEntity.setPossibleAnswers(possibleAnswers)

		updated = questionEntity.updateByPosition(db, position)

		if updated:
			db.close()
			return '', 200

		db.close()
		return 'Invalid position', 404

	#Retourner la réponse
	db.close()
	return 'Question does not exists', 404

@app.route('/questions/<position>', methods=['DELETE'])
def DeleteQuestion(position):
	
	if not AuthService().isAuthentificated():
		return 'Bad auth', 401

	#Supprimer la question de la base de données
	db = Database()

	if QuestionEntity.getByPosition(db, position, False):
		QuestionEntity.deleteByPosition(db, position)
		db.close()
		return '', 204

	#Retourner la réponse
	db.close()
	return 'Question does not exits', 404 

###> PARTICIPATION <###
@app.route('/participations', methods=['POST'])
def CreateParticipation():
	#Récupérer les données envoyées
	payload = request.get_json()

	#Ajouter la question à la base de données
	db = Database()
	
	#Création de la question
	score = ParticipationEntity.getScore(db,  payload["answers"])
	questionEntity = ParticipationEntity(payload["playerName"], score)
	created = questionEntity.create(db)
	
	if created:
		db.close()
		return questionEntity.toJson(), 200
		
	db.close()
	return 'Invalid answers number', 400

@app.route('/participations', methods=['DELETE'])
def DeleteAllParticipations():

	#Récupérer la base de données
	db = Database()
	
	#Création de la question
	deleted = ParticipationEntity.deleteAll(db)
	
	if deleted:
		db.close()
		return str(deleted), 204
		
	db.close()
	return 'Unable to delete all participations', 404

if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)