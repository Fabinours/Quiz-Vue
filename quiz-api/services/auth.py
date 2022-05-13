from flask import Flask, request
import jwt
import datetime
from werkzeug.exceptions import Unauthorized

class AuthService:

    def __init__(self):
        self.__secret = "Super secret key know one will ever know, right ?"
        self.__expiration_in_seconds = 10000

    def isAuthentificated(self, withoutExceptions = True):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """

        if (withoutExceptions):
            try:
                self.__auth()
            except:
                return False

        else:
            self.__auth()

        return True

    def __auth(self):
        #Récupération du token envoyé en paramètre
        headerTokenData = request.headers.get('Authorization')
        if not(headerTokenData):
            raise JwtError('Authorization header is empty.')

        headerTokenData = headerTokenData.split(' ')
        if not(2 <= len(headerTokenData)):
            raise JwtError('Authorization header is uncomplete.')

        # Vérification de la validité du token
        token = headerTokenData[1]
        try:
            payload = jwt.decode(token, self.__secret, algorithms="HS256")
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise JwtError('Signature expired. Please log in again.')
        except jwt.InvalidTokenError as e:
            raise JwtError('Invalid token. Please log in again.')

    def buildToken(self, pwd):
        """
        Generates the Auth Token
        :return: string
        """
        if(pwd != "Vive l'ESIEE !"):
            return '', 401

        token = jwt.encode(
            {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.__expiration_in_seconds),
                'iat': datetime.datetime.utcnow(),
                'sub': 'quiz-app-admin'
            },
            self.__secret,
            algorithm="HS256"
        )

        return {"token": token}, 200


class JwtError(Exception):
    """Exception raised for jwt errors in the quiz app 
    """

    def __init__(self, message="Jwt error"):
        self.message = message
        super().__init__(self.message)


