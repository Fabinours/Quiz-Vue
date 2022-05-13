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
        cur = db.getCursor()

        try:
            # start transaction
            cur.execute("begin")
            # add question
            cur.execute(f"INSERT INTO Question (Title, Text, Image, Position) VALUES ('{db.formatStr(self.title)}', '{db.formatStr(self.text)}', '{self.image}', '{self.position}')")

            #send the request
            cur.execute("commit")

            return cur.lastrowid

        except Exception as e:
            #in case of exception, roolback the transaction
            cur.execute('rollback')

    @staticmethod
    def positionExists(db : Database, questionId : int):
        """
        Verify if the question position is already used
        :param db:
        :return: true if exists, false else
        """
        cur = db.getCursor()
        cur.execute(f"SELECT Id FROM Question WHERE Position = {questionId}")
        return len(cur.fetchall()) != 0

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

            # add question
            cur.execute(f"DELETE Question WHERE Id={questionId}")

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
        return Question(json["title"], json["text"], json["image"], json["position"])
