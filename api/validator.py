from pydantic import BaseModel 


class AuthRequestSchema(BaseModel):
    username :str 
    password :str