from pydantic import BaseModel, ConfigDict, EmailStr, Field

class Author(BaseModel):
    name: str = Field(
        ...,
        min_length=5,
        max_length=30,
        description="Nombre del author (mínimo 5 caracteres)",
        examples=["John Doe"]
    )
    email: EmailStr = Field(
        ...,
        description="Correo electrónico del author",
        examples=["johndoe@example.com"]
    )
    
    model_config = ConfigDict(from_attributes=True)