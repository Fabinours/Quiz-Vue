from database import Database
import entities.answers as A

# Exemple de création de classe en python
class QuestionEntity():
    def __init__(self, title : str, text : str, image : str, position : int, possibleAnswers : list = None):
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.setPossibleAnswers(possibleAnswers)

    def setPossibleAnswers(self, possibleAnswers : list):
        self.possibleAnswers = None
        if possibleAnswers:
            self.possibleAnswers = possibleAnswers
            for possibleAnswer in self.possibleAnswers:
                possibleAnswer.questionEntity = self

    def __str__(self):
        return f"{self.title} : {self.text}"

    # >> INSERT / UPDATE / DELETE << #

    def create(self, db : Database):
        """
        Create a new question into the questions table
        :param db:
        :return: question id
        """

        if not(self.position in self.__getPossiblePositions(db)):
            return None

        try:
            cur = db.getCursor()

            # start transaction
            cur.execute("begin")

            # increment indexes
            cur.execute(f"UPDATE Question SET Position = - (Position + 1) WHERE Position >= {self.position}")
            cur.execute(f"UPDATE Question SET Position = - Position WHERE Position < 0")

            # add question
            cur.execute(f"INSERT INTO Question (Title, Text, Image, Position) VALUES ('{db.formatStr(self.title)}', '{db.formatStr(self.text)}', '{self.image}', '{self.position}')")

            # add possible answers
            for possibleAnswer in self.possibleAnswers:
                cur.execute(possibleAnswer.sqlCreate(db))

            #send the request
            cur.execute("commit")

            return cur.lastrowid

        except Exception as e:
            #in case of exception, roolback the transaction
            cur.execute('rollback')
            return None

    def __getPossiblePositions(self, db : Database):

        data = self.getAll(db)

        if not data:
            return [1]

        return list(range(1, len(data) + 2))

    def updateByPosition(self, db : Database, position : int):
        """
        Update the question related to the position
        :param db:
        :return: None
        """

        interval = self.__getPossiblePositions(db)
        interval[-1] -= 1

        if not(self.position in interval):
            print("Position not in interval")
            return False

        question = QuestionEntity.getByPosition(db, position)
        initialPosition = question.position
        finalPosition = self.position

        # try:

        cur = db.getCursor()

        # start transaction
        cur.execute("begin")

        # update possible answers
        cur.execute(A.AnswerEntity.sqlDeletePossibleAnswersOfQuestion(db, question))

        if(initialPosition > finalPosition):
            #store initial question at position 0 temporarily
            cur.execute(f"UPDATE Question SET Position = 0 WHERE Position = {initialPosition}")
            #increment positions
            cur.execute(f"UPDATE Question SET Position = - (Position + 1) WHERE Position < {initialPosition} AND Position >= {finalPosition} AND Position != 0")
            cur.execute(f"UPDATE Question SET Position = - Position WHERE Position < 0")
            #update initial question to final position
            cur.execute(f"UPDATE Question SET Position = {finalPosition} WHERE Position == 0")

        elif(initialPosition < finalPosition):
                #store initial question at position 0 temporarily
            cur.execute(f"UPDATE Question SET Position = 0 WHERE Position = {initialPosition}")
            #decrement positions
            cur.execute(f"UPDATE Question SET Position = - (Position - 1) WHERE Position > {initialPosition} AND Position <= {finalPosition}")
            cur.execute(f"UPDATE Question SET Position = - Position WHERE Position < 0")
            #update initial question to final position
            cur.execute(f"UPDATE Question SET Position = {finalPosition} WHERE Position == 0")

        # update question
        cur.execute(
            f"UPDATE Question SET "
            f" Title     = '{db.formatStr(self.title)}', "
            f" Text      = '{db.formatStr(self.text)}', "
            f" Image     = '{self.image}' "
            f" WHERE Position = {finalPosition} "
        )
        
        for possibleAnswer in self.possibleAnswers:
            cur.execute(possibleAnswer.sqlCreate(db))
        
        #send the request
        cur.execute("commit")

        return True

        # except Exception as e:
        #     # in case of exception, roolback the transaction
        #     cur.execute('rollback')

    @staticmethod
    def deleteByPosition(db : Database, position : int):
        """
        Delete a question into the questions table
        :param db:
        :param position
        :return: None
        """
        cur = db.getCursor()

        question = QuestionEntity.getByPosition(db, position)

        try:
            # start transaction
            cur.execute("begin")

            # delete possible answers
            cur.execute(A.AnswerEntity.sqlDeletePossibleAnswersOfQuestion(db, question))
            
            # delete question
            cur.execute(f"DELETE FROM Question WHERE Position = {position}")
            
            # decrement positions
            cur.execute(f"UPDATE Question SET Position = - (Position - 1) WHERE Position >= {position}")
            cur.execute(f"UPDATE Question SET Position = - Position WHERE Position < 0")
            
            #send the request
            cur.execute("commit")

            return cur.lastrowid

        except Exception as e:
            #in case of exception, roolback the transaction
            cur.execute('rollback')
    
    # >> GET << #

    @staticmethod
    def sqlGetIdFromPosition(db : Database, position : int):
        return f"(SELECT q.Id FROM Question q WHERE q.Position = '{position}')"

    @staticmethod
    def getByPosition(db : Database, position : int, withAnswers = True):
        """
        Get question from position
        :param db:
        :param position
        :param withAnswers=True
        :return: Question/None
        """
        cur = db.getCursor()
        # add question
        cur.execute(f"SELECT Title, Text, Image, Position from Question WHERE Position={position}") 

        # build the question
        question_data = cur.fetchone()

        if not question_data:
            return None

        questionEntity = QuestionEntity(question_data[0], question_data[1], question_data[2], question_data[3])
        if withAnswers:
            questionEntity.possibleAnswers = A.AnswerEntity.getPossibleAnswersOfQuestion(db, questionEntity)

        return questionEntity

    @staticmethod
    def getAll(db : Database, withAnswers = True):
        """
        Get all questions 
        :param db:
        :param withAnswers=True
        :return: Questions/None
        """
        cur = db.getCursor()
        # add question
        cur.execute(f"SELECT Title, Text, Image, Position from Question") 

        # build the question
        questions_data = cur.fetchall()

        if not questions_data:
            return None

        questionsEntities = []
        for question_data in questions_data:
            questionEntity = QuestionEntity(question_data[0], question_data[1], question_data[2], question_data[3])
            if withAnswers:
                questionEntity.possibleAnswers = A.AnswerEntity.getPossibleAnswersOfQuestion(db, questionEntity)
            questionsEntities.append(questionEntity)

        return questionsEntities

    # >> JSON << #
    def toJson(self):
        return {
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "position": self.position,
            "possibleAnswers": [ possibleAnswer.toJson() for possibleAnswer in self.possibleAnswers ] if self.possibleAnswers else []
        }
    
    @staticmethod
    def fromJson(json):
        return QuestionEntity(json["title"], json["text"], json["image"], json["position"])

    