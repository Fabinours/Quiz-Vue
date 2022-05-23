from database import Database
from entities.questions import QuestionEntity

# Exemple de création de classe en python
class ParticipationEntity():
    def __init__(self, playerName : str, score : int):
        self.playerName = playerName
        self.score = score

    @staticmethod
    def getScore(db : Database, answers : list):

        questions = QuestionEntity.getAll(db)

        if len(questions) != len(answers):
            return None

        score = 0
        for i in range(len(questions)):
            if answers[i] - 1 in questions[i].getGoodAnswers():
                score += 1

        return score

    def __str__(self):
        return f"{self.playerName} : {self.score}"

    # >> GETTERS << #
    def create(self, db : Database):
        """
        Create a new participation into the participations table
        :param db:
        :return: participation id
        """

        if self.score is None:
            return False

        try:

            cur = db.getCursor()

            # start transaction
            cur.execute("begin")

            # add participation
            cur.execute(f"INSERT INTO Participation (PlayerName, Score) VALUES ('{db.formatStr(self.playerName)}', {self.score})")

            #send the request
            cur.execute("commit")

            return cur.lastrowid

        except Exception as e:
            #in case of exception, roolback the transaction
            cur.execute('rollback')
            return None

    @staticmethod
    def deleteAll(db : Database):
        """
        Delete all the participations of the participations table
        :param db:
        :return: true or false
        """
        try:

            cur = db.getCursor()

            # start transaction
            cur.execute("begin")

            # add participation
            cur.execute(f"DELETE FROM Participation WHERE 1")

            #send the request
            cur.execute("commit")

            return True

        except Exception as e:
            #in case of exception, roolback the transaction
            cur.execute('rollback')
            return False

    @staticmethod
    def getAll(db : Database):
        """
        Get all the participations of the participations table
        :param db:
        :return: true or false
        """
        cur = db.getCursor()

        # add participation
        cur.execute(f"SELECT PlayerName, Score FROM Participation ORDER BY Score DESC")

        participationsData = cur.fetchall()
        return [ ParticipationEntity(participation[0], participation[1]) for participation in participationsData ]

    # >> JSON << #
    def toJson(self):
        return {
            "playerName": self.playerName,
            "score": self.score
        }
    
    @staticmethod
    def fromJson(json):
        return QuestionEntity(json["playerName"], json["score"])
