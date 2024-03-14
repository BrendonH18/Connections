import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from datetime import datetime, timedelta

User = get_user_model()

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):    
        token = self.extract_token(request=request)
        if token is None:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            self.verify_token(payload=payload)
            user_id = payload['id']
            user = User.objects.get(id=user_id)
            return (user, None)
        except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist) as e:
            raise AuthenticationFailed("Invalid token") from e


    def verify_token(self, payload):
        if 'exp' not in payload:
            raise InvalidTokenError("Token has no expiration")
        exp_timestamp = payload['exp']
        current_timestamp = datetime.utcnow().timestamp()
        if current_timestamp > exp_timestamp:
            raise ExpiredSignatureError("Token has expired")
    
    def extract_token(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None
    
    @database_sync_to_async
    def authenticate_websocket(self, scope, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            self.verify_token(payload=payload)
            user_id = payload['id']
            return User.objects.get(id=user_id)
        except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist) as e:
            raise AuthenticationFailed("Invalid token") from e


    
    @staticmethod
    def generate_token(payload):  # sourcery skip: aware-datetime-for-utc
        expiration = datetime.utcnow() + timedelta(hours=24)
        payload['exp'] = expiration
        return jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')