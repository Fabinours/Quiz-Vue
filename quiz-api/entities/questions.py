from database import Database

# Exemple de création de classe en python
class QuestionEntity():
    def __init__(self, title : str, text : str, image : str, position : int):
        self.title = title
        self.text = text
        self.image = image
        self.position = position

    def __str__(self):
        return f"{self.title} : {self.text}"

    # >> GETTERS << #

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

            #send the request
            cur.execute("commit")

            return cur.lastrowid

        except Exception as e:
            #in case of exception, roolback the transaction
            cur.execute('rollback')
            return None

    def update(self, db : Database, questionId : int):
        """
        Update the question related to the questionId
        :param db:
        :return: None
        """

        interval = self.__getPossiblePositions(db)
        interval[-1] -= 1

        if not(self.position in interval):
            return False

        initialPosition = QuestionEntity.get(db, questionId).position
        finalPosition = self.position

        try:

            cur = db.getCursor()

            # start transaction
            cur.execute("begin")

            # update indexes
            cur.execute(f"UPDATE Question SET Position = -1 WHERE Id = {questionId}")
            cur.execute(f"UPDATE Question SET Position = {initialPosition} WHERE Position == {finalPosition}")
            cur.execute(f"UPDATE Question SET Position = {finalPosition} WHERE Id == {questionId}")

            # add question
            cur.execute(
                f"UPDATE Question SET "
                f" Title     = '{db.formatStr(self.title)}', "
                f" Text      = '{db.formatStr(self.text)}', "
                f" Image     = '{self.image}', "
                f" Position  = {self.position} "
                f" WHERE Id = {questionId} "
            )

            #send the request
            cur.execute("commit")

            return True

        except Exception as e:
            # in case of exception, roolback the transaction
            cur.execute('rollback')

    def updateByPosition(self, db : Database, position : int):
        """
        Update the question related to the questionId
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

        try:

            cur = db.getCursor()

            # start transaction
            cur.execute("begin")
            print("1")
            # update indexes
            cur.execute(f"UPDATE Question SET Position = -1 WHERE Position = {initialPosition}")
            cur.execute(f"UPDATE Question SET Position = {initialPosition} WHERE Position = {finalPosition}")
            cur.execute(f"UPDATE Question SET Position = {finalPosition} WHERE Position = -1")
            print("2")
            # add question
            cur.execute(
                f"UPDATE Question SET "
                f" Title     = '{db.formatStr(self.title)}', "
                f" Text      = '{db.formatStr(self.text)}', "
                f" Image     = '{self.image}' "
                f" WHERE Position = {finalPosition} "
            )
            print("3")
            #send the request
            cur.execute("commit")

            return True

        except Exception as e:
            print(e)
            # in case of exception, roolback the transaction
            cur.execute('rollback')

    def __getPossiblePositions(self, db : Database):

        data = self.getAll(db)

        if not data:
            return [1]

        return list(range(1, len(data) + 2))

    @staticmethod
    def exists(db : Database, questionId : int):
        """
        Verify if the question id is not already used
        :param db:
        :return: true if exists, false else
        """
        cur = db.getCursor()
        cur.execute(f"SELECT Id FROM Question WHERE Id = {questionId}")
        return len(cur.fetchall()) != 0

    @staticmethod
    def delete(db : Database, questionId : int):
        """
        Delete a new question into the questions table
        :param db:
        :param questionId
        :return: None
        """
        cur = db.getCursor()

        try:
            # start transaction
            cur.execute("begin")

            position = QuestionEntity.get(db, questionId).position

            # add question
            cur.execute(f"DELETE FROM Question WHERE Id = {questionId}")

            # update indexes
            cur.execute(f"UPDATE Question SET Position = Position - 1 WHERE Position >= {position}")

            #send the request
            cur.execute("commit")

            return cur.lastrowid

        except Exception as e:
            #in case of exception, roolback the transaction
            cur.execute('rollback')

    @staticmethod
    def get(db : Database, questionId : int):
        """
        Get question from questionId
        :param db:
        :param questionId
        :return: Question/None
        """
        cur = db.getCursor()
        # add question
        cur.execute(f"SELECT Title, Text, Image, Position from Question WHERE Id={questionId}") 

        # build the question
        question_data = cur.fetchone()

        if not question_data:
            return None

        return QuestionEntity(question_data[0], question_data[1], question_data[2], question_data[3])

    @staticmethod
    def getByPosition(db : Database, position : int):
        """
        Get question from position
        :param db:
        :param position
        :return: Question/None
        """
        cur = db.getCursor()
        # add question
        cur.execute(f"SELECT Title, Text, Image, Position from Question WHERE Position={position}") 

        # build the question
        question_data = cur.fetchone()

        if not question_data:
            return None

        return QuestionEntity(question_data[0], question_data[1], question_data[2], question_data[3])


    @staticmethod
    def getAll(db : Database):
        """
        Get all questions 
        :param db:
        :return: Questions/None
        """
        cur = db.getCursor()
        # add question
        cur.execute(f"SELECT Title, Text, Image, Position from Question") 

        # build the question
        questions_data = cur.fetchall()

        if not questions_data:
            return None

        return list(map(lambda obj: QuestionEntity(obj[0], obj[1], obj[2], obj[3]), questions_data))

    # >> JSON << #
    def toJson(self):
        return {
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "position": self.position
        }
    
    @staticmethod
    def fromJson(json):
        return QuestionEntity(json["title"], json["text"], json["image"], json["position"])
