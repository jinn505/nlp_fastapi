from sqlalchemy.orm import Session
from database import *
from schemas import *
from main import *
from text_sentiment import *

def get_user(username : str,db : Session):
    return db.query(User).filter(User.username == username).first()

def create_user(username : str, hashed_password : str, db:Session):
    db_user = User(username=username, hashed_password=hashed_password)
    existing_user = get_user(username,db)
    if existing_user:
        return "user already exists"
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_description_for_user(desc_id: int, user_id: int, db: Session):
    return db.query(description).filter(description.task_id == desc_id, description.user_id == user_id).first()

def get_all_description_for_user(user_id : int, db:Session):
   return db.query(description).filter(description.user_id == user_id).all()

def create_question_for_user(user_id : int , ask : str , answer : str, db:Session):
   db_task = db.query(description).filter(description.question == ask).first()
   if db_task:
      return {"already asked"}
   new_task = description(
    question=ask,
    mood_description=answer,
    user_id=user_id
)
   db.add(new_task)
   db.commit()
   db.refresh(new_task)
   return new_task

def update_question_for_user(user_id : int , new_ques : str,desc_id : int, db:Session):
   db_desc = get_description_for_user(desc_id,user_id,db)
   if not db_desc:
      return {"question id does not exist"}
   db_desc.question = new_ques
   db_desc.mood_description = sentiment(db_desc.question)
   db.commit()
   db.refresh(db_desc)
   return db_desc

def delete_description_for_user(user_id : int ,desc_id : int, db:Session):
   db_desc = get_description_for_user(desc_id,user_id,db)
   if not db_desc:
      return {"question id does not exist"}
   db.delete(db_desc)
   db.commit()
   return db_desc