import jwt
from datetime import datetime, timedelta

SECRET = '26ee0962f82f5bcf62da6be588a751df7656725c083fa8a50c390f6392f2a2d7'
ALGORITHM = 'HS256'
EXPIRATION_TIME = 10

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode['exp'] = datetime.now() + timedelta(minutes=EXPIRATION_TIME)
    # to_encode.update({'expiration_time': datetime.now() + timedelta(minutes=EXPIRATION_TIME)})
    
    jwt_token = jwt.encode(payload=to_encode, key=SECRET, algorithm=ALGORITHM)
    
    return jwt_token