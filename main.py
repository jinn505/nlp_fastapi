from fastapi import FastAPI,Depends,HTTPException,Response
from schemas import *
from text_sentiment import *
from database import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import relationship,Session
from crud import *
from auth import *



Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

db_dependency = Annotated[Session , Depends(get_db)]

@app.post("/create")
def register(user : loginmodel,db:db_dependency):
    existing_user = get_user(user.username,db)
    if existing_user:
        return "user already registered"
    hashed_password = hash_password(user.password)
    new_user = create_user(user.username,hashed_password,db)
    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    return {"message" : "user added successfully"}

@app.post("/login",response_model=Token)
def login(db:db_dependency,response : Response,form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    user = get_user(username,db)
    if not user:
        raise HTTPException(status_code=401, detail="credentials not found")
    elif not verify_password(password , user.hashed_password):
        raise HTTPException(status_code=404, detail="invalid credentials")
    
    token = create_access_token({"sub" : username})
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(db:db_dependency,access_token: str = Depends(oauth2_scheme)):
    payload = decode_token(access_token)
    print(payload)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = get_user(username, db)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user

@app.post("/classify-sentiment/")  
def questions(input : classify,db:db_dependency, current_user: str = Depends(get_current_user)):
    tokens =  tokenize(input.text)
    spacy_tokens, named_entities = lemmatize(input.text)
    cleaned_text = " ".join(spacy_tokens)
    response = sentiment(cleaned_text)
    new_creation = create_question_for_user(current_user.user_id,input.text,response,db)

    return {
      "message" : "question asked"
    } 

@app.get("/classify-sentiment/")  
def answers(db:db_dependency, current_user: str = Depends(get_current_user)):
    return get_all_description_for_user(current_user.user_id,db)

