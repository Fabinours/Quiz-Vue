from database import Database
import entities.questions as Q

# Exemple de création de classe en python
class AnswerEntity():
    def __init__(self, text : str, isCorrect : bool, questionEntity : Q.QuestionEntity = None):
        self.questionEntity = questionEntity
        self.text = text
        self.isCorrect = isCorrect

    def __str__(self):
        return f"{self.text} : {self.isCorrect}"

    # >> GETTERS << #

    def sqlCreate(self, db : Database):
        """
        Return the SQL request to create a new answer into the answers table
        :param db:
        :return: question id
        """
        questionIdSql = Q.QuestionEntity.sqlGetIdFromPosition(db, self.questionEntity.position)
        insertSql = f"INSERT INTO Answer (QuestionId, Text, IsCorrect) VALUES ({questionIdSql}, '{db.formatStr(self.text)}', {1 if self.isCorrect else 0})"
        return insertSql

    @staticmethod
    def getPossibleAnswersOfQuestion(db : Database, questionEntity : Q.QuestionEntity):
        """
        Get the possible answers from a question
        :param db:
        :param questionEntity
        :return: Answer[]/None
        """

        cur = db.getCursor()

        # add question
        questionId = Q.QuestionEntity.sqlGetIdFromPosition(db, questionEntity.position)
        cur.execute(f"SELECT Text, IsCorrect from Answer WHERE QuestionId={questionId}") 

        # build the question
        answers_data = cur.fetchall()

        if not answers_data:
            return None

        return list(map(lambda obj : AnswerEntity(obj[0], obj[1], questionEntity), answers_data))

    @staticmethod
    def sqlDeletePossibleAnswersOfQuestion(db : Database, questionEntity : Q.QuestionEntity):
        """
        Get the SQL request to delete the answers from a question
        :param db:
        :param questionEntity
        :return: string
        """

        questionId = Q.QuestionEntity.sqlGetIdFromPosition(db, questionEntity.position)
        return f"DELETE FROM Answer WHERE QuestionId={questionId}"

    # >> JSON << #
    def toJson(self):
        return {
            "text": self.text,
            "isCorrect": True if self.isCorrect == 1 else False,
        }
    
    @staticmethod
    def fromJson(json):
        return AnswerEntity(json["text"], json["isCorrect"])
