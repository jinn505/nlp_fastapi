from sqlalchemy import create_engine, Column, Integer, String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapped_column,Mapped, relationship

db_url = "sqlite:///./responses.db"
engine = create_engine(db_url, connect_args={"check_same_thread": False})
sessionlocal = sessionmaker(autocommit = False,autoflush=False, bind = engine)

Base = declarative_base()

class description(Base):
    __tablename__ = "user_input" 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question : Mapped[str] = mapped_column(String, index = True)
    mood_description : Mapped[str] = mapped_column(String, index = True)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("user_data.user_id"))
    owner = relationship("User", back_populates="tasks")

class User(Base):
    __tablename__ = "user_data"
    user_id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username : Mapped[str] = mapped_column(String,nullable = False,index = True)
    hashed_password : Mapped[str] = mapped_column(String, nullable=False)
    tasks = relationship("description", back_populates="owner") 
