from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, TokenResponse
from app.auth.auth_utils import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()



@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


# @router.post("/login", response_model=TokenResponse)
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.email == user.email).first()

#     if not db_user or not verify_password(user.password, db_user.password_hash):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token({"sub": db_user.email})

#     return {
#         "access_token": token,
#         "token_type": "bearer"
#     }

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user or not verify_password(
        user.password, db_user.password_hash
    ):
        raise HTTPException(status_code=401)

    token = create_access_token({"sub": db_user.email})
    print(token)

    return {
        "access_token": token,
        "token_type": "bearer"
    }