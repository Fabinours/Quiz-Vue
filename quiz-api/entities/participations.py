from database import Database

# Exemple de création de classe en python
class ParticipationEntity():
    def __init__(self, playerName : str):
        self.playerName = playerName

    def __str__(self):
        return f"{self.playerName}"

    # >> GETTERS << #
    def create(self, db : Database):
        """
        Create a new participation into the participations table
        :param db:
        :return: participation id
        """
        try:

            cur = db.getCursor()

            # start transaction
            cur.execute("begin")

            # add participation
            cur.execute(f"INSERT INTO Participation (PlayerName) VALUES ('{db.formatStr(self.playerName)}')")

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
        cur.execute(f"SELECT PlayerName FROM Participation")

        return cur.fetchall()