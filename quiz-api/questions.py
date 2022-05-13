# Exemple de création de classe en python
class Question():
    def __init__(self, title : str, text : str, image : str):
        self.title = title
        self.text = text
        self.image = image

    def __str__(self):
        return f"{self.title} : {self.text}"

    def toJson(self):
        return {
            "title": self.title,
            "text": self.text,
            "image": self.image
        }
    
    @staticmethod
    def fromJson(json):
        return Question(json["title"], json["text"], json["image"])
