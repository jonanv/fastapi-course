from pydantic import BaseModel, Field, ConfigDict


class CateogyBase(BaseModel):
    name: str = Field(min_length=2, max_length=60)
    slug: str = Field(min_length=2, max_length=60)
    
class CategoryCreate(CateogyBase):
    pass

class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=60)
    slug: str | None = Field(default=None, min_length=2, max_length=60)
    
class CategoryPublic(BaseModel):
    id: int
    
    model_config = ConfigDict(from_attributes=True) # Permite que el modelo de Pydantic lea los datos desde los atributos como si fuera objetos de ORM 