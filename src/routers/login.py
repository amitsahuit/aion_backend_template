from tools import password_verification
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from ..schemas.login_schema import Token
from sqlalchemy.orm import Session
from tools import password_verification
from ..models import model
from tools import oAuth2


router = APIRouter(prefix="/login", tags=["LOGIN"])


@router.post("/", response_model=Token)
def login(
    inputVal: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # result = db.query(model.User).filter(model.User.email == inputVal.email).first()
    result = db.query(model.User).filter(model.User.email == inputVal.username).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"user with emil ID {inputVal.username} is not present",
        )

    if not password_verification.verification(inputVal.password, result.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials"
        )

    access_token = oAuth2.create_access_token(data={"user_id": result.id})
    return {"access_token": access_token, "token_type": "bearer"}
