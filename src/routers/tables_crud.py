############################ Without spliting models ############################
from fastapi import status, APIRouter, Depends
from ..database import engine, get_db
from ..models.model import Base, ShoppingCart, Product, User
from sqlalchemy.orm import session


router = APIRouter(prefix="/table", tags=["TABLES CRUD"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_table():
    # Create the database tables when the application starts
    Base.metadata.create_all(bind=engine)

    return {
        "message": "This is to create tables for the first time. If tables already present then run --> alembic upgrade head"
    }


@router.get("/", status_code=status.HTTP_200_OK)
async def get_tables(db: session = Depends(get_db)):
    user_list = db.query(User).all()
    product_list = db.query(Product).all()
    shopping_cart_list = db.query(ShoppingCart).all()
    return {
        "User": user_list,
        "Product": product_list,
        "ShoppingCart": shopping_cart_list,
    }


############################ With splited models ############################
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# # from ..models import shopping_cart_model
# # from ..models import user_model
# # from ..models import product_model
# from ..models.shopping_cart_model import ShoppingCart
# from ..models.user_model import User
# from ..models.product_model import Product
# from ..config import setting

# # Set up the database URL
# DATABASE_URL = f"postgresql://{setting.DATABASE_USERNAME}:{setting.DATABASE_PASSWORD}@{setting.DATABASE_HOSTNAME}:{setting.DATABASE_PORT}/{setting.DATABASE_NAME}"

# # Create a database engine
# engine = create_engine(DATABASE_URL)

# # product_model.Base.metadata.create_all(bind=engine)
# # user_model.Base.metadata.create_all(bind=engine)
# # shopping_cart_model.Base.metadata.create_all(bind=engine)
# # create the session

# Session = sessionmaker(bind=engine)
# session = Session()

# # create the tables
# Base.metadata.create_all(engine)
