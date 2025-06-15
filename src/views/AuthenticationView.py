from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Security
from services.AuthenticationService import AuthenticationService
from schemas.response.BaseResponse import BaseResponse
from schemas.request.AuthenticationRequests import CreateUser
from enums.RoleEnum import Role
from schemas.response.AuthenticationResponses import Token

router_authentication = APIRouter() 
_service = AuthenticationService()

@router_authentication.post("/user", summary="User Creation", response_model=BaseResponse)  
def create_user(data: CreateUser):
    """
    Endpoint for creating a new user.

    - **name**: User's name.
    - **email**: Unique email address.
    - **password**: User's password (stored using bcrypt hash).
    - **gender**: User's gender.
    - **ethnicity**: User's ethnicity.
    - **age**: User's age.

    Returns:
    - Success or error message.
    - Enrollment number of the created user, if successful.
    """
    return BaseResponse(message="Success", data="User successfully enrolled!", datas=_service.create_user(data))

@router_authentication.post("/login", summary="User Login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint for user login.

    - **enrollment**: User's registration number.
    - **password**: User's password (hashed and compared with stored hash).

    Returns:
    - Success or error message.
    - Token
    """
    return Token(access_token=_service.login(form_data), token_type="bearer")

@router_authentication.delete("/user", summary="User Deletion", response_model=BaseResponse)  
def delete_user(id_user: str, token: str = Security(_service.check_security, scopes=[Role.GESTOR.name])): 
    """
    Endpoint for deleting a user.

    Returns:
    - Success or error message.
    """
    return BaseResponse(message="Success", data=_service.delete_user(id_user))

@router_authentication.put("/role", summary="Update Role", response_model=BaseResponse)
def add_role(id_user: str, roles: list[Role], token: str = Security(_service.check_security, scopes=[Role.GESTOR.name])):
    """
    Endpoint for adding roles to a user.

    Returns:
    - Success or error message.
    """
    return BaseResponse(message="Success", data=_service.add_role(id_user, roles))

