from typing import Annotated, List, Optional
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import jwt
from models.User import User
from fastapi import Form, HTTPException, status
from repositories.IUser import IUser
from schemas.request.AuthenticationRequests import CreateUser, LoginRequest

from decouple import config
import bcrypt
from datetime import datetime, timedelta, timezone
import hashlib
from enums.RoleEnum import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", scopes={
    Role.STUDENT.name: str(Role.STUDENT.value),
    Role.GESTOR.name: str(Role.GESTOR.value)
}
)

class OAuth2CustomRequestForm:
    def __init__(self, enrollment: str = Form(...), password: str = Form(...)):
        self.enrollment = enrollment
        self.password = password

class AuthenticationService:
    def __init__(self):
        self.__user_repository = IUser()
        self.SECRET_KEY = config("SECRET_KEY")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))
        self.ALGORITHM = config("ALGORITHM")
        

    # -------------------------------- Repository access methods --------------------------------
    def create_user(self, request: CreateUser) -> dict:
        try:
            request.password = self.__hash_password(request.password)
            enrollment = self.__generate_enrollment(request)
            user_data = request.model_dump(exclude_unset=True)
            _user = User(**user_data, enrollment=enrollment)
            self.__user_repository.create(_user, roles=[Role.STUDENT.value])
            return {"enrollment": enrollment} 

        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    def login(self, request: OAuth2CustomRequestForm) -> str:
        try:
            user = self.__user_repository.find_by_enrollment(request.username)
            if user and bcrypt.checkpw(request.password.encode('utf-8'), user.password.encode('utf-8')):
                access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = self.__create_access_token(
                    data={"sub": user.enrollment},
                    expires_delta=access_token_expires,
                )
                return access_token
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    def delete_user(self, id_user: str) -> str:
        try:
            self.__user_repository.delete(id_user)
            return "User deleted successfully"

        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))
        
    def add_role(self, id_user: str, list: list[Role]):
        try:
            self.__user_repository.update_roles(id_user, [role.value for role in list])
            return "Roles updated successfully"

        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))
    # -------------------------------- Security functions --------------------------------

    def check_security (self, security_scopes: SecurityScopes, token:  Annotated[str, Depends(oauth2_scheme)]) -> str:
        try:
            # Decoding the token
            payload = self.decodeToken(token)
            # Enrollment verification
            enrollment: Optional[str] = payload.get("sub")
            if enrollment is None: 
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
            # Roles verification
            roles: Optional[list[Role]] = self.__user_repository.find_roles_by_enrollment(enrollment)
            if roles is None: 
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User has no roles.")
            if not any(role.name in security_scopes.scopes for role in roles):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
            return token
        
        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))
    
    def decodeToken(self, token):
        return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

    def __create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
        
    def __hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()  # Generates a random salt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)  # Encrypts the password
        return password_hash.decode('utf-8')
    
    # Enrollment format = year + hash(date_of_registration)[4] + hash(name)[4]
    def __generate_enrollment(self, data: CreateUser) -> str:
        year = datetime.now().year
        hash_date = hashlib.sha256(datetime.now().isoformat().encode()).hexdigest()[:4]
        hash_name = hashlib.sha256(data.name.encode()).hexdigest()[:4]
        enrollment = str(year) + hash_date + hash_name
        return enrollment