from fastapi import APIRouter, HTTPException, status
from database.database import SessionDep
from .models import Users
from .schemas import UserCreate, UserLogin, Token, RefreshToken, UserPublic
from .utils import get_password_hash
from datetime import timedelta
from .utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
import jwt
from .utils import verify_password
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic)
def register(user: UserCreate, session: SessionDep):
    if session.query(Users).filter(Users.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    if session.query(Users).filter(Users.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username уже зарегистрирован")
    if user.password != user.password2:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")

    new_user = Users(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login_for_access_token(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user_from_db = session.query(Users).filter(Users.username == form_data.username).first()
    
    if not user_from_db or not verify_password(form_data.password, user_from_db.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_from_db.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



@router.post("/refresh", response_model=Token)
def refresh(data: RefreshToken):
    try:
        payload = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Недопустимый refresh-токен")
    except:
        raise HTTPException(status_code=401, detail="Недопустимый refresh-токен")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



