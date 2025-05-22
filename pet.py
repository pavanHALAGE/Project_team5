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

