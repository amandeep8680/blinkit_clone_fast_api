from sqlalchemy import(
     Column, Integer, String, Boolean, DateTime ) 
from sqlalchemy.sql import func 
from app.database.database import Base
import uuid

class User(Base): 
    ''' this is super admin wil values name , email ,, password_hash is_active , 
            created_at , updated_at.  He is the one who create branches manager's '''

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True ,autoincrement=True,)
    unique_id = Column(String, unique=True, nullable = False, index=True ,default= lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    
    email = Column(String(255), unique=True, nullable=False, index=True)

    password_hash = Column(String(255), nullable=False)

    role = Column(String(50),nullable=False,default="super_admin",
                  )
    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
