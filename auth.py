from datetime import datetime, timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext

secret_key = "hello_everyone"
algo = "HS256"
access_token_expiry_minutes = 30

def create_access_token(data : dict, expiry_time : timedelta = None):
    data_copy = data.copy()
    expire_time = datetime.utcnow() + (expiry_time or timedelta(minutes=access_token_expiry_minutes))
    data_copy.update({"exp" : expire_time})
    return jwt.encode(data_copy,secret_key,algorithm=algo)

def decode_token(token:str):
    try:
        return jwt.decode(token,secret_key,algorithms=[algo])
    except JWTError:
        return None
    
def hash_password(plain_password : str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(plain_password)    
        
def verify_password(plain_password : str,hashed_password:str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password,hashed_password)   