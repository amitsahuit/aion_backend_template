from fastapi import Body, Response, status, APIRouter, Depends, HTTPException
from typing import Dict, Union, List
from src.database import get_db
from sqlalchemy.orm import Session
from ..models.model import User
from ..schemas.user_schema import UserCreate, UserResponse
from tools.password_verification import hash
from tools.oAuth2 import get_current_user

router = APIRouter(prefix="/user", tags=["USER CRUD"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
    address: str,
    married_status: bool,
    password: str,
    response: Response = None,
    user: UserCreate = Body(...),
    db: Session = Depends(get_db),
    get_current_userID: int = Depends(get_current_user),
) -> Dict[str, Union[str, int, bool, List[str]]]:
    inp_user = user.dict()

    # hashing password
    hashed_password = hash(password)

    inp_user.update(
        address=address, married_status=married_status, password=hashed_password
    )

    # inp_user.update(address=address, married_status=married_status, password=password)

    if inp_user["age"] < 18 and married_status:
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="BRO, it's too early you are just {inp_user['age']} years old. check with your Mom",
        )
    user_dict = User(**inp_user)
    db.add(user_dict)
    db.commit()
    db.refresh(user_dict)
    return inp_user


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_users_by_id(
    id: int,
    db: Session = Depends(get_db),
    get_current_userID: int = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User not found")
    return user


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    db: Session = Depends(get_db), get_current_userID: int = Depends(get_current_user)
):
    user = db.query(User).all()
    return user


# delete User
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(
    id: int,
    db: Session = Depends(get_db),
    get_current_userID: int = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


# update User
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_user(
    id: int,
    user: UserCreate = Body(...),
    db: Session = Depends(get_db),
    get_current_userID: int = Depends(get_current_user),
):
    user_result = db.query(User).filter(User.id == id)
    if user_result.first() == None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User not found")
    user_result.update(user.dict(), synchronize_session=False)
    db.commit()
    db.refresh(user_result.first())
    return {"message": "User updated successfully"}
