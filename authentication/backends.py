from django.contrib.auth.backends import BaseBackend
import psycopg2
from authentication.models import User
from utils import DatabaseConnection

database = DatabaseConnection()

class AuthBackend(BaseBackend):
    def authenticate(self, username=None, password=None):
        user: User = self.get_user(username)
        if user and user.password == password:
            return user
        return None

    def get_user(self, username):
        getUserQuery = f"select distinct * from pengguna where username='{username}'"
        queryResult = database.query(getUserQuery)
        if queryResult:
            queryResultUsername = queryResult[0]['username']
            queryResultPassword = queryResult[0]['password']
            queryResultNegaraAsal = queryResult[0]['negara_asal']
            return User(queryResultUsername, queryResultPassword, queryResultNegaraAsal)
        return None
    
    def login(self, request, user: User):
        request.session['user'] = {
            'username': user.username,
            'negara_asal': user.negara_asal
        }

    def logout(self, request):
        request.session.clear()

    def register(self, username, password, negara_asal):
        insertUserQuery = f"insert into pengguna values ('{username}', '{password}', '{negara_asal}')"
        queryResult = database.query(insertUserQuery)
        if isinstance(queryResult, psycopg2.errors.RaiseException):
            return queryResult
        return None
        
        
