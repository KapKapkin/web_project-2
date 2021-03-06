import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta


class AuthHandler():
	security = HTTPBearer()
	pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

	secret = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCIE6a1NyEFe7qCDFrvWFZiAlY1ttE5596w5dLjNSaHlKGv8AXbKg/f8yKY9fKAJ5BKoeWEkPPjpn1t9QQAZYzqH9KNOFigMU8pSaRUxjI2dDvwmu8ZH6EExY+RfrPjQGmeliK18iFzFgBtf0eH3NAW3Pf71OZZz+cuNnVtE9lrYQIDAQAB"

	def encode_token(self, email, type):
		payload = dict(
			sub = email,
			token_type = type
		)
		to_encode = payload.copy()
		if type == "access_token":
			to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=10)})
		else:
			to_encode.update({"exp": datetime.utcnow() + timedelta(hours=720)})

		return jwt.encode(to_encode, self.secret, algorithm='HS256')

	def encode_login_token(self, email):
		access_token = self.encode_token(email, "access_token")
		refresh_token = self.encode_token(email, "refresh_token")

		login_token = dict(
			access_token=f"{access_token}",
			refresh_token=f"{refresh_token}"
		) 
		return login_token

	def encode_update_token(self, email):
		access_token = self.encode_token(email, "access_token")

		update_token = dict(
			access_token=f"{access_token}"
		) 
		return update_token


	def decode_access_token(self, token):
		try:
			payload = jwt.decode(token, self.secret, algorithms=['HS256'])
			if payload['token_type'] != "access_token":
				raise HTTPException(status_code=401, detail='Invalid token')
			return payload['sub']
		except jwt.ExpiredSignatureError:
			raise HTTPException(status_code=401, detail='Sinature has expired')
		except jwt.InvalidTokenError as e:
			raise HTTPException(status_code=401, detail='Invalid token')

	def decode_refresh_token(self, token):
		try:
			payload = jwt.decode(token, self.secret, algorithms=['HS256'])
			if payload['token_type'] != "refresh_token":
				raise HTTPException(status_code=401, detail='Invalid token')
			return payload['sub']
		except jwt.ExpiredSignatureError:
			raise HTTPException(status_code=401, detail='Sinature has expired')
		except jwt.InvalidTokenError as e:
			raise HTTPException(status_code=401, detail='Invalid token')


	def auth_access_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
		return self.decode_access_token(auth.credentials)


	def auth_refresh_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
		return self.decode_refresh_token(auth.credentials)