from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserRegister, UserLogin
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        daily_study_hours=user.daily_study_hours
    )

    # Save user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    print("EMAIL:", user.email)
    print("FOUND USER:", db_user)

    if db_user:
        print("HASH:", db_user.hashed_password)
        print(
            "PASSWORD VALID:",
            verify_password(
                user.password,
                db_user.hashed_password
            )
        )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "user_id": db_user.id,
            "email": db_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "daily_study_hours": current_user.daily_study_hours
    }