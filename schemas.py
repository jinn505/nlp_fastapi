from pydantic import BaseModel, Field

class classify(BaseModel):
    text : str = Field(... , description="hey let me guess your mood ")

class loginmodel(BaseModel):
    username : str
    password : str    

class Token(BaseModel):
     access_token : str
     token_type : str    
