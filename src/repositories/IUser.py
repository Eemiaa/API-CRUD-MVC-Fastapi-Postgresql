import json
from typing import List
from bson import ObjectId
from fastapi import HTTPException
from configs.database import get_db
from models.User import User
from enums.RoleEnum import Role

class IUser:
    def __init__(self):
        self.session = next(get_db())["llmextension"]["user"]

    def create(self, user: User, roles: List[int]):
        try:
            data = user.model_dump(exclude_unset=True)
            data["roles"] = roles
            self.session.insert_one(data)

        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    def find_by_enrollment(self, enrollment: str) -> User:
        try:
            json_user = self.session.find_one({"enrollment": enrollment})
            if not json_user:
                raise HTTPException(status_code=404, detail="User not found.")
            return User(**json_user)
        
        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))
        
    def find_id_by_enrollment(self, enrollment: str) -> str:
        try:
            json_user = self.session.find_one({"enrollment": enrollment})
            if not json_user:
                raise HTTPException(status_code=404, detail="User not found.")
            return json_user['_id']
        
        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    def find(self, user_id: int) -> User:
        try:
            json_user = self.session.find_one({"_id": ObjectId(user_id)})
            if not json_user:
                raise HTTPException(status_code=404, detail="User not found.")
            return User(**json_user)
        
        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))
        
    def find_roles_by_enrollment(self, enrollment: str) -> List[Role]:
        try:
            json_user = self.session.find_one({"enrollment": enrollment})
            if not json_user:
                raise HTTPException(status_code=404, detail="User not found.")
            user = User(**json_user)
            return user.roles
        
        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))
              
    def find_all(self) -> List[User]:
        try:
            json_users = self.session.find()
            return [User(**user) for user in json_users]
        
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    def delete(self, user_id: int) -> bool:
        try:
            existing_user = self.session.find_one({"_id": ObjectId(user_id)})
            if not existing_user:
                raise HTTPException(status_code=404, detail="User not found.")
            self.session.delete_one({"_id": ObjectId(user_id)})
            return True
        
        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    def update_roles(self, user_id: int, roles:list[str]):
        try:
            existing_user = self.session.find_one({"_id": ObjectId(user_id)})

            if not existing_user:
                raise HTTPException(status_code=404, detail="User not found.")
            
            existing_user['roles'] = roles
            
            self.session.update_one({"_id": ObjectId(user_id)}, {"$set": existing_user})

        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

