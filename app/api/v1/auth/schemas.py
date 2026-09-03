from pydantic import BaseModel

from ..user.schemas import UserPublic
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
    
class TokenData(BaseModel):
    sub: str
    username: str