#added by utkarsh
from sqlalchemy import Column, Integer, String



from db.database import Base



class User(Base):
    __tablename__ = 'users'


    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey



from db.database import Base



class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)







from pydantic import BaseModel, EmailStr




class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str



class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


from pydantic import BaseModel



from datetime import date



class ExpenseCreate(BaseModel):
    amount: float
    category: str
    date: date
    description: str
    user_id: int

#good code


class ExpenseOut(BaseModel):
    id: int
    amount: float
    category: str
    date: date
    description: str
    user_id: int

    class Config:
        orm_mode = True

#DB CONNECT


from sqlalchemy import create_engine


from sqlalchemy.ext.declarative import declarative_base



from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./expenses.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



#QUARY OPERATION

from sqlalchemy.orm import Session



from models import user, expense



from schemas import user_schema, expense_schema




# User Operations



def create_user(db: Session, user_data: user_schema.UserCreate):
    db_user = user.User(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password  # Note: In production, hash the password!
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_user_by_email(db: Session, email: str):
    return db.query(user.User).filter(user.User.email == email).first()




# Expense Operations



def create_expense(db: Session, expense_data: expense_schema.ExpenseCreate):
    db_expense = expense.Expense(
        amount=expense_data.amount,
        category=expense_data.category,
        date=expense_data.date,
        description=expense_data.description,
        user_id=expense_data.user_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense




def get_expenses_by_user(db: Session, user_id: int):
    return db.query(expense.Expense).filter(expense.Expense.user_id == user_id).all()

#main 

from db.database import SessionLocal, Base, engine


from db import queries



from schemas import user_schema, expense_schema


from datetime import date



# Create the database tables
Base.metadata.create_all(bind=engine)





def main():
    db = SessionLocal()

   
    
    
    # Create a new user
    new_user = user_schema.UserCreate(
        username="john_doe",
        email="john@example.com",
        password="securepassword"
    )
    user = queries.create_user(db, new_user)
    print(f"User created: {user.username}")

    
    
    
    # Add an expense for the user
    new_expense = expense_schema.ExpenseCreate(
        amount=50.0,
        category="Groceries",
        date=date.today(),
        description="Weekly grocery shopping",
        user_id=user.id
    )
    expense = queries.create_expense(db, new_expense)
    print(f"Expense added: {expense.description} - ${expense.amount}")

   
    
    
   
    # Retrieve all expenses for the user
    expenses = queries.get_expenses_by_user(db, user.id)
    print(f"Expenses for {user.username}:")
    for exp in expenses:
        print(f"{exp.date} - {exp.category}: ${exp.amount} - {exp.description}")








if __name__ == "__main__":
   
    
    
    
    main()




